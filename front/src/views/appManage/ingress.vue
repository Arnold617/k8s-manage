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
      <el-table-column prop="serverName" label="Service" align="center" min-width="15%">
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

    <!--新增界面-->
		<el-dialog title="新增" v-model="addFormVisible" :close-on-click-modal="false">
			<el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
        <el-form-item label="namespace" prop="namespace">
          <el-select v-model="addForm.namespace" filterable placeholder="请选择空间">
						<el-option v-for="ns in NameSpaceList" :key="ns" :label="ns" :value="ns"></el-option>
					</el-select>
        </el-form-item>
        <el-form-item label="名称" prop="name">
					<el-input v-model.trim="addForm.name" :change="check_addName()" auto-complete="off" placeholder="名称"></el-input>
				</el-form-item>
        <el-form-item label="域名" prop="host">
					<el-input v-model="addForm.host" :min="100" :max="9999" placeholder="域名" />
          <span style="color:red">多个域名用逗号','分开</span>
				</el-form-item>
        <el-form-item label="路径" prop="path">
					<el-input v-model="addForm.path" :min="100" :max="9999" placeholder="path" />
          <span style="color:red">全域名用"/"即可</span>
				</el-form-item>
        <el-form-item label="Service" prop="serverName">
          <el-input v-model="addForm.serverName" placeholder="Service" />
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
    import { getIngressList, deleteIngress, addIngress, updateIngress, getNameSpaces } from '../../api/api';

  export default {
    data() {
      return {
        filters: {
					name: ''
				},
        appList: [],
        listLoading: false,
        addLoading: false,
        addFormVisible: false,
        NameSpaceList: [],
        page: 1,
        total: 0,
        select_value: '',
        addForm: {
          name: '',
        },
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

      check_addName: function() {
        this.addForm.name = this.addForm.name.replace(/[^\a-z\0-9\_\-]/g,'');
      },
      //显示新增界面
      handleAdd: function() {
				this.addFormVisible = true;
			},
    }
  }
</script>