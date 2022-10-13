<template>
  <section>
    <!-- 工具条 -->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true" :model="filters">
				<el-form-item>
					<el-button type="success" @click="handleAdd">+</el-button>
				</el-form-item>
				<el-form-item>
					<el-input v-model="filters.name" placeholder="查询deployment"></el-input>
				</el-form-item>
			</el-form>
		</el-col>

    <el-table :data="appList" highlight-current-row v-loading="listLoading" style="width: 100%;">
			<el-table-column type="index" label="ID" width="66px"></el-table-column>
			<el-table-column prop="name" label="名称" min-width="15%">
			</el-table-column>
      <el-table-column prop="replicas" label="副本数" align="center" min-width="10%">
				<template slot-scope="scope">
					<el-tag type="success" disable-transitions>{{scope.row.replicas}}</el-tag>
				</template>
			</el-table-column>
      <el-table-column prop="containerPort" label="容器端口" align="center" min-width="12%">
				<template slot-scope="scope">
					<el-tag type="success" disable-transitions>{{scope.row.containerPort}}</el-tag>
				</template>
			</el-table-column>
			<el-table-column prop="imageUrl" label="镜像版本" align="center" min-width="40%">
			</el-table-column>
			<el-table-column label="操作" align="center" width="260px">
				<template slot-scope="scope">
					<el-button type="primary" size="small" @click="handleDetail(scope.$index, scope.row)">进入</el-button>
					<el-button type="warning" size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
					<el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>
					<el-button type="success" size="small" @click="handlePut(scope.$index, scope.row)">发布</el-button>
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
				<el-form-item label="副本数" prop="replicas">
					<el-input-number v-model="addForm.replicas" :min="1" :max="99" placeholder="副本数量"></el-input-number>
				</el-form-item>
        <el-form-item label="容器端口" prop="containerPort">
					<el-input-number v-model="addForm.containerPort" :min="1" :max="65535" placeholder="窗口端口"></el-input-number>
				</el-form-item>
        <el-form-item label="核心数(m)" prop="cpuLimit">
					<el-input-number v-model="addForm.cpuLimit" :min="100" :max="9999" placeholder="cpu"></el-input-number>
          <span style="color:red">1000m = 1核</span>
				</el-form-item>
        <el-form-item label="内存数(Mi)" prop="memoryLimit">
					<el-input-number v-model="addForm.memoryLimit" :min="100" :max="9999" placeholder="memory"></el-input-number>
          <span style="color:red">1024Mi = 1G</span>
				</el-form-item>
        <el-form-item label="镜像版本" prop="imageUrl">
					<el-input v-model="addForm.imageUrl" auto-complete="off" placeholder="镜像版本"></el-input>
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
					<el-input v-model="editForm.name" auto-complete="off" readonly></el-input>
				</el-form-item>
        <el-form-item label="副本数" prop="replicas">
					<el-input-number v-model="editForm.replicas" :min="1" :max="99"></el-input-number>
				</el-form-item>
        <el-form-item label="容器端口" prop="containerPort">
					<el-input-number v-model="editForm.containerPort" :min="1" :max="65535"></el-input-number>
				</el-form-item>
        <el-form-item label="核心数(m)" prop="cpuLimit">
					<el-input-number v-model="editForm.cpuLimit" :min="100" :max="9999"></el-input-number>
          <span style="color:red">1000m = 1核</span>
				</el-form-item>
        <el-form-item label="内存数(Mi)" prop="memoryLimit">
					<el-input-number v-model="editForm.memoryLimit" :min="100" :max="9999"></el-input-number>
          <span style="color:red">1024Mi = 1G</span>
				</el-form-item>
				<el-form-item label="镜像版本" prop="imageUrl">
					<el-input v-model="editForm.imageUrl" auto-complete="off" style="50%"/>
				</el-form-item>
        <el-form-item label="环境变量" prop="env">
					<el-input v-model="editForm.env" auto-complete="off" style="50%"/>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="editFormVisible = false">取消</el-button>
				<el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
			</div>
		</el-dialog>

		<!-- 版本发布 -->
		<el-dialog title="版本发布" customClass="customWidth" v-model="versionFormVisible" :close-on-click-modal="false">
			<el-form :model="versionForm" label-width="80px" :rules="versionFormRules" ref="versionForm">
				<el-form-item label="项目名称" prop="name">
					<el-input v-model="versionForm.name" style="width:40%" auto-complete="off" :disabled="true"></el-input>
				</el-form-item>
				<el-form-item label="镜像版本" prop="imageUrl">
					<el-input v-model="versionForm.imageUrl" auto-complete="off"	></el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="versionFormVisible = false">取消</el-button>
				<el-button type="primary" @click.native="putSubmit" :loading="versionLoading">提交</el-button>
			</div>
		</el-dialog>

  </section>
</template>
<script>
  import { getDeploymentList, deleteDeployment, addDeployment, updateDeployment } from '../../api/api';
  export default {
    data() {
      return {
        filters: {
					name: ''
				},
        total: 0,
        queryData: '',
        appList: [],
        listLoading: false,
        editLoading: false,
				versionLoading: false,
        addForm: {
          name: '',
        },
        editForm: {},
				versionForm: {},
        editFormVisible: false,
        addFormVisible: false, //新增界面是否显示
				versionFormVisible: false,
				addLoading: false,
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
				},
        editFormRules: {
          name: [{
						required: true,
						message: '请输入名称',
						trigger: 'blur'
					}],
          imageUrl: [{
						required: true,
						message: '请输入',
						trigger: 'blur'
					}],
        },
				versionFormRules: {
					imageUrl: [{
						required: true,
						message: '输入版本号',
						trigger: 'blur'
					}]
				}

      }
    },

    created() {
      this.get_applist()
    },

    methods: {

      handleCurrentChange(val) {
				this.page = val;
				this.get_applist();
			},
      // 限制只能输入数字，英文
      check_addName: function() {
        this.addForm.name = this.addForm.name.replace(/[^\a-z\0-9\_\-]/g,'');
      },

      get_applist() {
				this.listLoading = true;
        this.queryData = this.$route.query
        let params = {
					nameSpace: this.queryData.nameSpace,
					projectName: this.queryData.projectName
				}
        getDeploymentList(params)
          .then(res => {
            this.appList = res.data.data;
            this.total = res.data.count;
						this.listLoading = false;
          })
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

			// 显示版本发布界面
			handlePut: function(index, row) {
				this.versionFormVisible = true;
				this.versionForm = Object.assign({}, row);
			},

      //添加
			addSubmit: function() {
				this.$refs.addForm.validate((valid) => {
					if (valid) {
						this.$confirm('确认提交吗？', '提示', {
							type: 'warning'
						}).then(() => {
							this.addLoading = true;
							let params = Object.assign({}, this.addForm);
              params['nameSpace'] = this.queryData.nameSpace;
              params['projectName'] = this.queryData.projectName;
              // console.log(this.queryData)
							addDeployment(params)
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
						});
					}
				});
			},

      // 编辑
			editSubmit: function() {
				this.$refs.editForm.validate((valid) => {
					if (valid) {
						this.$confirm('确认提交吗？', '提示', {
							type: 'warning'
						}).then(() => {
							this.editLoading = true;
							const params = Object.assign({}, this.editForm);
							updateDeployment(params)
								.then((res) => {
									this.editLoading = false;
									this.$message({
										message: '提交成功',
										type: 'success'
									});
									this.$refs['editForm'].resetFields();
									this.editFormVisible = false;
									this.get_applist();
								});
						});
					}
				});
			},

      //删除
			handleDel: function(index, row) {
				this.$confirm('确认删除该deployment吗?', '提示', {
					type: 'warning',
				}).then(() => {
					this.listLoading = true;
					deleteDeployment(row)
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

			// 版本发布
			putSubmit: function() {
				this.versionLoading = true;
				const params = Object.assign({}, this.versionForm);
				updateDeployment(params)
					.then((res) => {
						this.versionLoading = false;
						this.$message({
							message: '提交成功',
							type: 'success'
						});
						this.$refs['versionForm'].resetFields();
						this.versionFormVisible = false;
						this.get_applist();
					})
			},

			//跳到详情页面
			handleDetail: function(index, row) {
				this.$router.push({
					path: 'podDetail',
					query: {
						namespace: row.nameSpace,
						name: row.name
					}
				})
				// console.log(row);
			},

    },

  }

</script>
<style>
  .customWidth{
   width:35%;
}
 </style>