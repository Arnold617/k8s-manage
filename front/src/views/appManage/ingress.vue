<template>
  <section>
    <!-- 工具条 -->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true" :model="filters">
				<el-form-item>
					<el-button type="success" @click="handleAdd">+</el-button>
				</el-form-item>
				<el-form-item>
					<el-input v-model="filters.name" placeholder="查询应用名称"></el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" v-on:click="get_applist">查询</el-button>
				</el-form-item>
				<el-form-item style="margin-left: 50%;">
					<el-select v-model="select_value" clearable filterable placeholder="请选择空间" @change=get_applist()>
						<el-option v-for="ns in NameSpaceList" :key="ns" :label="ns" :value="ns"></el-option>
					</el-select>
				</el-form-item>
			</el-form>
		</el-col>

    <el-table :data="appList" highlight-current-row v-loading="listLoading" style="width: 100%;">
			<el-table-column type="index" label="ID" width="66px"></el-table-column>  
      <el-table-column prop="name" label="项目名" align="center" min-width="15%" >
			</el-table-column>
      <el-table-column prop="namespace" label="命名空间" align="center" min-width="15%" >
			</el-table-column>
      <el-table-column prop="host" label="域名" align="center" min-width="15%">
			</el-table-column>
      <el-table-column prop="path" label="路径" align="center" min-width="15%">
			</el-table-column>
      <el-table-column prop="serviceName" label="Service" align="center" min-width="15%">
			</el-table-column>
      <el-table-column prop="servicePort" label="Port" align="center" min-width="15%">
			</el-table-column>
      <el-table-column label="操作" align="center" width="200px">
        <template slot-scope="scope">
          <el-button type="warning" size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
          <el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>
        </template>
        <template>
          <div id="xterm" class="xterm"></div>
        </template>
      </el-table-column>
		</el-table>

    <!--页脚-->
		<el-col :span="24" class="toolbar">
			<el-pagination @current-change="handleCurrentChange" :page-size="15" layout="total, prev, pager, next" :total="total">
			</el-pagination>
		</el-col>

    <!--新增界面-->
		<el-dialog title="新增" v-model="addFormVisible" :close-on-click-modal="false">
			<el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
        <el-form-item label="namespace" prop="namespace">
          <el-select v-model="addForm.namespace" clearable="" filterable placeholder="请选择空间" @change=get_servicelist()>
						<el-option v-for="ns in NameSpaceList" :key="ns" :label="ns" :value="ns"></el-option>
					</el-select>
        </el-form-item>
        <el-form-item label="名称" prop="name">
					<el-input v-model.trim="addForm.name" :change="check_addName()" auto-complete="off" placeholder="名称"></el-input>
				</el-form-item>
        <el-form-item label="域名" prop="host">
					<el-input v-model="addForm.host" placeholder="域名" />
          <span style="color:red">多个域名用逗号','分开</span>
				</el-form-item>
        <el-form-item label="路径" prop="path">
					<el-input v-model="addForm.path" placeholder="path" />
          <span style="color:red">全路径用"/"即可</span>
				</el-form-item>
        <el-form-item label="Service" prop="serviceName">
          <el-select v-model="addForm.serviceName" clearable filterable placeholder="请选择">
						<el-option v-for="ns in serviceList" :key="ns.name" :label="ns.name" :value="ns.name+','+ns.port"></el-option>
					</el-select>
        </el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="addFormVisible = false">取消</el-button>
				<el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
			</div>
		</el-dialog>

    <!--编辑界面-->
		<el-dialog title="编辑" v-model="editFormVisible" :close-on-click-modal="false">
			<el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
				<el-form-item label="项目名" prop="name">
					<el-input v-model="editForm.name" auto-complete="off"/>
				</el-form-item>
        <el-form-item label="命令空间" prop="namespace">
					<el-input v-model="editForm.namespace" disabled auto-complete="off"/>
				</el-form-item>
        <el-form-item label="域名" prop="host">
          <el-input v-model="editForm.host" auto-complete="off" />
          <span style="color:red">多个域名用逗号','分开</span>
        </el-form-item>
        <el-form-item label="路径" prop="path">
          <el-input v-model="editForm.path" />
          <span style="color:red">全路径用"/"即可</span>
        </el-form-item>
				<el-form-item label="Service" prop="serviceName">
					<el-input v-model="editForm.serviceName" disabled auto-complete="off"/>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="editFormVisible = false">取消</el-button>
				<el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
			</div>
		</el-dialog>

  </section>
</template>
<script>
    import { getIngressList, deleteIngress, addIngress, updateIngress, getNameSpaces, getServiceList, } from '../../api/api';

  export default {
    data() {
      return {
        filters: {
					name: ''
				},
        appList: [],
        listLoading: false,
        addLoading: false,
        editLoading: false,
        addFormVisible: false,
        editFormVisible: false,
        NameSpaceList: [],
        serviceList: [],
        page: 1,
        total: 0,
        select_value: '',
        addForm: {
          name: '',
        },
        editForm: {},
        addFormRules: {
					name: [{
						required: true,
						message: '请输入名称',
						trigger: 'blur'
					}],
          host: [{
						required: true,
						message: '请输入名称',
						trigger: 'blur'
					}],
          path: [{
						required: true,
						message: '请输入名称',
						trigger: 'blur'
					}],
        },
        editFormRules: {
					name: [{
						required: true,
						message: '请输入名称',
						trigger: 'blur'
					}],
          host: [{
						required: true,
						message: '请输入名称',
						trigger: 'blur'
					}],
          path: [{
						required: true,
						message: '请输入名称',
						trigger: 'blur'
					}],
        },

      }

    },

    created() {
      this.get_namespace()
      this.get_applist()
    },

    methods: {

      get_namespace() {
				getNameSpaces()
					.then(res => {
						this.NameSpaceList = res.data.namespace_list
					})
			},

      get_applist() {
        this.listLoading = true;
        let params = {
					namespace: this.select_value,
				}
        getIngressList(params)
          .then(res => {
            this.appList = res.data.data;
						this.total = res.data.count;
						this.listLoading = false;
          })
      },

      get_servicelist() {
        let params = {
          namespace: this.addForm.namespace,
        }
        getServiceList(params)
          .then(res => {
            this.serviceList = res.data.data;
          })
      },

      handleCurrentChange(val) {
				this.page = val;
				this.get_applist();
			},

      check_addName: function() {
        this.addForm.name = this.addForm.name.replace(/[^\a-z\0-9\_\-]/g,'');
      },
      //显示新增界面
      handleAdd: function() {
				this.addFormVisible = true;
			},

      // 显示编辑界面
			handleEdit: function(index, row) {
				this.editFormVisible = true;
				this.editForm = Object.assign({}, row);
			},

      //添加
			addSubmit: function() {
        this.addLoading = true;
        let params = Object.assign({}, this.addForm);
        let serviceInfo = params.serviceName
        params.serviceName = serviceInfo.split(',')[0]
        params.servicePort = serviceInfo.split(',')[1]
        addIngress(params)
          .then((res) => {
            this.addLoading = false;
            this.$message({
              message: '提交成功',
              type: 'success'
            });
            this.$refs['addForm'].resetFields();
            this.addFormVisible = false;
            this.get_applist();
          });		
			},

      // 编辑
			editSubmit: function() {
        this.editLoading = true;
        const params = Object.assign({}, this.editForm);
        updateIngress(params)
          .then((res) => {
            this.editLoading = false;
            this.$message({
              message: '提交成功',
              type: 'success'
            });
            this.$refs['editForm'].resetFields();
            this.editFormVisible = false;
            this.get_applist();
					})
			},

      handleDel: function(index, row) {
				this.$confirm('确认删除该Ingress吗?', '提示', {
					type: 'warning',
				}).then(() => {
					this.listLoading = true;
					deleteIngress(row)
						.then((res) => {
							this.listLoading = false;
							this.$message({
								message: '删除成功',
								type: 'success'
							});
							this.get_applist();
						});
				}).catch(() => {});
			},

    }
  }
</script>