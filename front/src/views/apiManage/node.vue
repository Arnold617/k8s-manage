<template>
  <section>
    <!-- 工具条 -->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true">
				<el-form-item>
					<el-input v-model="selectVal" icon="search" class="search" placeholder="查询节点名称"></el-input>
				</el-form-item>
			</el-form>
		</el-col>

    <el-table :data="tables" highlight-current-row v-loading="listLoading" style="width: 100%;">
			<el-table-column type="index" label="ID" width="66px"></el-table-column>  
      <el-table-column prop="name" label="名称" align="center" min-width="15%" >
			</el-table-column>
      <el-table-column prop="status" label="状态" align="center" min-width="15%">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status | statusFilter"> {{scope.row.status}} </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="ip" label="IP" align="center" min-width="15%" >
			</el-table-column>
      <el-table-column prop="memory_percent" label="内存" align="center" min-width="15%">
        <template slot-scope="scope">
        <el-progress :text-inside="true" :stroke-width="22" :percentage="scope.row.memory_percent*100" status="success"/>
      </template>
      </el-table-column>
      <el-table-column prop="kubelet_version" label="kubelet_version" align="center" min-width="15%">
			</el-table-column>
      <el-table-column prop="os_image" label="os_image" align="center" min-width="15%">
			</el-table-column>
      <el-table-column label="操作" align="center" width="200px">
        <template slot-scope="scope">
          <el-button type="warning" size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
          <el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
		</el-table>

    <el-col :span="24" class="toolbar">
			<!-- <el-pagination @current-change="handleCurrentChange" :page-size="15" layout="total, prev, pager, next" :total="total">
			</el-pagination> -->
		</el-col>
    
  </section>
</template>

<script>
import { getNodeList } from '../../api/api'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        Ready: 'success',
        NotReady: 'danger'
      }
      return statusMap[status]
    }
  },
  
  data() {
    return {
      selectVal: '',
      nodeList: [],
      listLoading: false,
    }
  },

  created() {
    this.get_nodelist()
  },

  computed: {
    tables() {
      var selectVal = this.selectVal
      // console.log(selectVal)
      if (selectVal) {
        return this.nodeList.filter(dataNews => {
          return Object.keys(dataNews).some(key => {
            return String(dataNews[key]).indexOf(selectVal) > -1  //区分大小写，严格搜索对应
          })
        })
      }
      return this.nodeList
    }
  },

  methods: {
    get_nodelist() {
      this.listLoading = true
      getNodeList()
        .then(res => {
          this.nodeList = res.data.data
          this.listLoading = false
        })
    },
  }

}
</script>
