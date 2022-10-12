<template>
  <section>
    <!-- 工具条 -->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true">
				<el-form-item>
          <el-button type="warning" @click="handleScaling" circle>容器伸缩</el-button>
          <el-button type="primary" @click="handlePut" circle>版本发布</el-button>
					<el-button type="success" @click="get_podlist" circle>刷新页面</el-button>
				</el-form-item>
			</el-form>
		</el-col>

    <el-table :data="podList" highlight-current-row v-loading="listLoading" style="width: 100%;">
			<el-table-column type="index" label="ID" width="66px"></el-table-column>  
      <el-table-column prop="ip" label="容器ip" align="center" min-width="15%" >
			</el-table-column>
      <el-table-column prop="node" label="宿主机" align="center" min-width="15%">
			</el-table-column>
      <el-table-column prop="status" label="容器状态" align="center" min-width="15%">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status | statusFilter"> {{scope.row.status}} </el-tag>
        </template>
      </el-table-column>
			<el-table-column label="启动时间" align="center" min-width="20%">
        <template slot-scope="scope">
					{{scope.row.startTime|parseDate}}
				</template>
			</el-table-column>
      <el-table-column label="操作" align="center" width="100px">
        <template slot-scope="scope">
          <el-button type="warning" size="small" @click="handleDetail(scope.$index, scope.row)">>__</el-button>
        </template>
        <template>
          <div id="xterm" class="xterm"></div>
        </template>
      </el-table-column>
		</el-table>

    <!-- 伸缩容器 -->
    <el-dialog title="伸缩pod" customClass="customWidth" v-model="scalingFormVisible" :close-on-click-modal="false">
			<el-form :model="scalingForm" label-width="80px" :rules="scalingFormRules" ref="scalingForm">
				<el-form-item label="项目名称" prop="name">
					<el-input v-model="scalingForm.name" style="width:40%" auto-complete="off" :disabled="true"></el-input>
				</el-form-item>
				<el-form-item label="容器数量" prop="replicas">
					<el-input-number v-model="scalingForm.replicas"></el-input-number>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="scalingFormVisible = false">取消</el-button>
				<el-button type="primary" @click.native="scalingPod" :loading="scalingLoading">提交</el-button>
			</div>
		</el-dialog>

    <!-- 版本发布 -->
		<el-dialog title="版本发布" customClass="customWidth" v-model="versionFormVisible" :close-on-click-modal="false">
			<el-form :model="scalingForm" label-width="80px" :rules="versionFormRules" ref="versionForm">
				<el-form-item label="项目名称" prop="name">
					<el-input v-model="scalingForm.name" style="width:40%" :disabled="true"></el-input>
				</el-form-item>
				<el-form-item label="镜像版本" prop="imageUrl">
					<el-input v-model="scalingForm.imageUrl" auto-complete="off"	></el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="versionFormVisible = false">取消</el-button>
				<el-button type="primary" @click.native="versionPut" :loading="versionLoading">提交</el-button>
			</div>
		</el-dialog>


  </section>
</template>
<script>
  import { getPodList, getDeploymentList, updateDeployment } from '../../api/api';
  // import 'xterm/css/xterm.css';
  // import { Terminal } from 'xterm';
  // import { FitAddon } from 'xterm-addon-fit';
  // import { AttachAddon } from 'xterm-addon-attach';
  import moment from 'moment-timezone';

  export default{
    filters:{
			parseDate(val) {
				if (val != '' && val){
					return moment(val).format('YYYY-MM-DD HH:mm:ss')
				}
			},
      statusFilter(status) {
        const statusMap = {
          Running: 'success',
          Pending: 'danger'
        }
        return statusMap[status]
      }
		},

    data() {
      return {
        queryData: '',
        podList: [],
        deploymentData: {},
        listLoading: false,
        versionLoading: false,
        scalingForm: {},
        // versionForm: {},
        scalingLoading: false,
        scalingFormVisible: false,
        
        versionFormVisible: false,
        scalingFormRules: {},
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
      this.get_podlist();
    },

    methods: {

      get_podlist() {
        this.listLoading = true;
        this.queryData = this.$route.query
        let params = {
          namespace: this.queryData.namespace,
          name: this.queryData.name
        }
        getPodList(params)
          .then(res => {
            this.podList = res.data.data;
            this.listLoading = false;
          })
      },

      get_deployment() {
        getDeploymentList(this.queryData)
          .then((res) => {
            this.scalingForm = res.data.data[0]
          })
      },

      // 显示伸缩pod界面
      handleScaling: function(index, row) {
				this.scalingFormVisible = true;
        this.get_deployment()
			},

      // 显示版本发布界面
			handlePut: function(index, row) {
				this.versionFormVisible = true;
        this.get_deployment();
			},

      // 伸缩pod
			scalingPod: function() {
        this.scalingLoading = true;
        const params = Object.assign({}, this.scalingForm);
        updateDeployment(params)
          .then((res) => {
            this.scalingLoading = false;
            this.$message({
              message: '提交成功',
              type: 'success'
            });
            this.$refs['scalingForm'].resetFields();
            this.scalingFormVisible = false;
            this.get_podlist();
          });
			},
      
      // 版本发布
      versionPut: function() {
        this.versionLoading = true;
        const params = Object.assign({}, this.scalingForm);
        updateDeployment(params)
          .then((res) => {
            this.versionLoading = false;
            this.$message({
              message: '提交成功',
              type: 'success'
            });
            this.$refs['scalingForm'].resetFields();
            this.versionFormVisible = false;
            this.get_podlist();
          });
			},
      
    }
  }
</script>
<style>
  .customWidth{
   width:35%;
}
 </style>