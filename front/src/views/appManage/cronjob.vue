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
      <el-table-column prop="schedule" label="计划时间" align="center" min-width="15%">
			</el-table-column>
      <el-table-column prop="imageUrl" label="镜像地址" align="center" min-width="15%">
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
    
    <!--工具条-->
		<el-col :span="24" class="toolbar">
			<el-pagination @current-change="handleCurrentChange" :page-size="15" layout="total, prev, pager, next" :total="total">
			</el-pagination>
		</el-col>

    <!--新增界面-->
		<el-dialog title="新增" v-model="addFormVisible" :close-on-click-modal="false">
			<el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
				<el-form-item label="名称" prop="name">
					<el-input v-model.trim="addForm.name" :change="check_addName()" auto-complete="off" placeholder="名称"></el-input>
				</el-form-item>
        <el-form-item label="namespace" prop="namespace">
          <el-select v-model="addForm.namespace" filterable placeholder="请选择空间">
						<el-option v-for="ns in NameSpaceList" :key="ns" :label="ns" :value="ns"></el-option>
					</el-select>
        </el-form-item>
        <el-form-item label="核心数(m)" prop="cpuLimit">
					<el-input-number v-model="addForm.cpuLimit" :min="100" :max="9999" placeholder="cpu"></el-input-number>
          <span style="color:red">1000m = 1核</span>
				</el-form-item>
        <el-form-item label="内存数(Mi)" prop="memoryLimit">
					<el-input-number v-model="addForm.memoryLimit" :min="100" :max="9999" placeholder="memory"></el-input-number>
          <span style="color:red">1024Mi = 1G</span>
				</el-form-item>
        <el-form-item label="镜像地址" prop="imageUrl">
          <el-input v-model="addForm.imageUrl" placeholder="镜像地址"></el-input>
        </el-form-item>
        <el-form-item label="调度计划" prop="schedule">
					<el-input v-model="addForm.schedule" auto-complete="off" placeholder="* * * * * (分时日月周)"></el-input>
				</el-form-item>
        <el-form-item label="执行命令" prop="command">
					<el-input v-model="addForm.command" auto-complete="off" placeholder="执行命令"></el-input>
				</el-form-item>
        <el-form-item label="环境变量" prop="env">
					<el-input v-model="addForm.env" auto-complete="off" placeholder="环境变量"></el-input>
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
				<el-form-item label="项目名称" prop="name">
					<el-input v-model="editForm.name" auto-complete="off" readonly />
				</el-form-item>
        <el-form-item label="核心数(m)" prop="cpuLimit">
          <el-input-number v-model="editForm.cpuLimit" />
          <span style="color:red">1000m = 1核</span>
        </el-form-item>
        <el-form-item label="内存数(Mi)" prop="memoryLimit">
          <el-input-number v-model="editForm.memoryLimit" />
          <span style="color:red">1024Mi = 1G</span>
        </el-form-item>
				<el-form-item label="镜像地址" prop="imageUrl">
					<el-input v-model="editForm.imageUrl" auto-complete="off" style="50%"/>
				</el-form-item>
        <el-form-item label="调度计划" prop="schedule">
          <el-input v-model="editForm.schedule" auto-complete="off"/>
        </el-form-item>
        <el-form-item label="执行命令" prop="command">
          <el-input v-model="editForm.command" auto-complete="off"/>
        </el-form-item>
        <el-form-item label="环境变量" prop="env">
          <el-input v-model="editForm.env" auto-complete="off"/>
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
  import { getCronJobList, deleteCronJob, addCronJob, updateCronJob, getNameSpaces } from '../../api/api';

  export default {
    filters:{
			parseDate(val) {
				if (val != '' && val){
					return moment(val).format('YYYY-MM-DD HH:mm:ss')
				}
			}
    },

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
        page: 1,
        total: 0,
        select_value: '',
        addForm: {
          name: '',
        },
        editForm: {
          name: '',
        },
        
        addFormRules: {
					name: [{
						required: true,
						message: '请输入名称',
						trigger: 'blur'
					}],
					imageUrl: [{
						required: true,
						message: '请输入镜像URL',
						trigger: 'blur'
					}],
          command: [{
						required: true,
						message: '请输入命令',
						trigger: 'blur'
					}],
          schedule: [{
						required: true,
						message: '请输入调试计划',
						trigger: 'blur'
					}],
				},
        editFormRules: {
					name: [{
						required: true,
						message: '请输入名称',
						trigger: 'blur'
					}],
					imageUrl: [{
						required: true,
						message: '请输入镜像URL',
						trigger: 'blur'
					}],
          command: [{
						required: true,
						message: '请输入命令',
						trigger: 'blur'
					}],
          schedule: [{
						required: true,
						message: '请输入调试计划',
						trigger: 'blur'
					}],
				},

      }
    },
    created() {
      this.get_applist()
      this.get_namespace()
    },

    methods: {
      
      get_applist() {
        this.listLoading = true;
        let params = {
					namespace: this.select_value,
				}
        getCronJobList(params)
          .then(res => {
            this.appList = res.data.data;
						this.total = res.data.count;
						this.listLoading = false;
          })
      },

      get_namespace() {
				getNameSpaces()
					.then(res => {
						this.NameSpaceList = res.data.namespace_list
					})
			},

      handleCurrentChange(val) {
				this.page = val;
				this.get_applist();
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

      // 限制只能输入数字，英文
      check_addName: function() {
        this.addForm.name = this.addForm.name.replace(/[^\a-z\0-9\_\-]/g,'');
      },

      //添加
			addSubmit: function() {
        this.addLoading = true;
        let params = Object.assign({}, this.addForm);
        addCronJob(params)
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
        updateCronJob(params)
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
				this.$confirm('确认删除该cronjob吗?', '提示', {
					type: 'warning',
				}).then(() => {
					this.listLoading = true;
					deleteCronJob(row)
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