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
					<el-select v-model="select_value" filterable placeholder="请选择空间" clearable @change=get_applist()>
						<el-option v-for="ns in NameSpaceList" :key="ns" :label="ns" :value="ns"></el-option>
					</el-select>
				</el-form-item>
			</el-form>
		</el-col>

		<!--列表-->
		<el-table :data="appList" highlight-current-row v-loading="listLoading" style="width: 100%;">
			<el-table-column type="index" label="ID" width="80px"></el-table-column>
			<el-table-column prop="projectName" label="项目名称" align="center" min-width="20%">
			</el-table-column>
			<el-table-column prop="nameSpace" label="命名空间" align="center" min-width="20%">
			</el-table-column>
			<el-table-column prop="imageUrl" label="镜像地址" align="center" min-width="30%">
			</el-table-column>
			<el-table-column label="操作" align="center" width="200px">
				<template slot-scope="scope">
					<el-button type="warning" size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
					<el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>
					<el-button type="primary" size="small" @click="handleDetail(scope.$index, scope.row)">进入</el-button>
				</template>
			</el-table-column>
		</el-table>

		<!--工具条-->
		<el-col :span="24" class="toolbar">
			<el-pagination @current-change="handleCurrentChange" :page-size="15" layout="total, prev, pager, next" :total="total">
			</el-pagination>
		</el-col>

		<!--编辑界面-->
		<el-dialog title="编辑" v-model="editFormVisible" :close-on-click-modal="false">
			<el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
				<el-form-item label="ID" prop="id">
					<el-input v-model="editForm.id" readonly></el-input>
				</el-form-item>
				<el-form-item label="项目名称" prop="projectName">
					<el-input v-model="editForm.projectName" auto-complete="off" readonly></el-input>
				</el-form-item>
				<el-form-item label="镜像地址" prop="imageUrl">
					<el-input v-model="editForm.imageUrl" auto-complete="off" style="50%" readonly/>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="editFormVisible = false">取消</el-button>
				<el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
			</div>
		</el-dialog>

		<!--新增界面-->
		<el-dialog title="新增" v-model="addFormVisible" :close-on-click-modal="false">
			<el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
				<el-form-item label="项目名称" prop="projectName">
					<el-input v-model="addForm.projectName" auto-complete="off" placeholder="项目名称"></el-input>
				</el-form-item>
				<el-form-item label="镜像地址" prop="imageUrl">
					<el-input v-model="addForm.imageUrl" auto-complete="off" placeholder="镜像地址"></el-input>
				</el-form-item>
				<el-form-item label="集群空间" prop="nameSpace">
					<el-select v-model="addForm.nameSpace" filterable placeholder="请选择空间">
						<el-option v-for="ns in NameSpaceList" :key="ns" :label="ns" :value="ns"></el-option>
					</el-select>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="addFormVisible = false">取消</el-button>
				<el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
			</div>
		</el-dialog>

	</section>
</template>

<script>

import { getNameSpaces, getPodList, getAppList, deleteApp, addApp, updateApp } from '../../api/api';

	export default {
		data() {
			return {
				filters: {
					name: ''
				},
				appList: [],
				NameSpaceList: [],
				total: 0,
				page: 1,
				select_value: '',
				listLoading: false,
				editFormVisible: false, //编辑界面是否显示
				editFormRules: {
					projectName: [{
						required: true,
						message: '请输入',
						trigger: 'blur'
					}],
					imageUrl: [{
						required: true,
						message: '请输入',
						trigger: 'blur'
					}]
				},
				//编辑界面数据
				editForm: {
					id: 0,
				},
				editLoading: false,

				addFormVisible: false, //新增界面是否显示
				addLoading: false,
				addFormRules: {
					projectName: [{
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
				//新增界面数据
				addForm: {
					projectName: '',
				},
			}
		},
		created() {
			this.get_namespace()
			this.get_applist()
		},

		methods: {
			handleCurrentChange(val) {
				this.page = val;
				this.get_applist();
			},

			get_namespace() {
				getNameSpaces()
					.then(res => {
						this.NameSpaceList = res.data.namespace_list
					})
			},
			get_applist() {
				this.listLoading = true;
				let params = {
					nameSpace: this.select_value,
					projectName: this.filters.name
				}
				getAppList(params)
					.then(res => {
						this.appList = res.data.data;
						this.total = res.data.count;
						this.listLoading = false;
					})
			},

			// selectChange() {
			// 	getPodList(params)
			// 		.then(res => {
			// 			this.appList = res.data.data
			// 			// console.log(res.data)
			// 		})
			// },

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
				this.$refs.addForm.validate((valid) => {
					if (valid) {
						this.$confirm('确认提交吗？', '提示', {
							type: 'warning'
						}).then(() => {
							this.addLoading = true;
							let params = Object.assign({}, this.addForm);
							addApp(params)
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
							updateApp(params)
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
						})
					}
				});
			},

			//删除
			handleDel: function(index, row) {
				this.$confirm('确认删除该记录吗?', '提示', {
					type: 'warning',
				}).then(() => {
					this.listLoading = true;
					deleteApp(row)
						.then((res) => {
							this.listLoading = false;
							this.$message({
								message: '删除成功',
								type: 'success'
							});
							this.get_applist();
						});
				}).catch(() => {
					this.$message({
            type: 'warning',
            message: '已取消删除'
					});
				});
			},

			//跳到详情页面
			handleDetail: function(index, row) {
				this.$router.push({
					path: '/appDetail',
					query: {
						nameSpace: row.nameSpace,
						projectName: row.projectName
					}
				})
			},
		}
	}
</script>

<style>
</style>
