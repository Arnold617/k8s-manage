<template>
    <div style=";font-weight:bold">
        <el-row :gutter="16">
            <el-col :span="6">
                <el-card class="card" :loading="dashLoading" :hoverable="true" style="background-color: rgb(72, 209,141);">
                    <div class="ant-statistic-title" style="font-size:20px" align="center">集群</div>
                    <div class="ant-statistic-content" align="center">
                        <span style="font-size:40px">{{ dataList.clusters }}</span>
                        <span style="font-size:20px">个</span>
                    </div>
                </el-card>
            </el-col>

            <el-col :span="6">
                <el-card class="card" :loading="dashLoading" :hoverable="true" style="background-color: rgb(249, 89, 89);">
                    <div class="ant-statistic-title" style="font-size:20px" align="center">主机</div>
                    <div class="ant-statistic-content" align="center">
                        <span style="font-size:40px">{{ dataList.nodes }}</span>
                        <span style="font-size:20px">台</span>
                    </div>
                </el-card>
            </el-col>

            <el-col :span="6">
                <el-card class="card" :loading="dashLoading" :hoverable="true" style="background-color: rgb(133,149,244);">
                    <div class="ant-statistic-title" style="font-size:20px" align="center">应用</div>
                    <div class="ant-statistic-content" align="center">
                        <span style="font-size:40px">{{ dataList.apps }}</span>
                        <span style="font-size:20px">个</span>
                    </div>
                </el-card>
            </el-col>

            <el-col :span="6">
                <el-card class="card" :loading="dashLoading" :hoverable="true" style="background-color: rgb(254,187,80);">
                    <div class="ant-statistic-title" style="font-size:20px" align="center">定时任务</div>
                    <div class="ant-statistic-content" align="center">
                        <span style="font-size:40px">{{ dataList.cronjobs }}</span>
                        <span style="font-size:20px">个</span>
                    </div>
                </el-card>
            </el-col>

            <el-col :span="6">
                <el-card class="card" :loading="dashLoading" :hoverable="true" style="background-color: gold">
                    <div class="ant-statistic-title" style="font-size:20px" align="center">NameSpaces</div>
                    <div class="ant-statistic-content" align="center">
                        <span style="font-size:40px">{{ dataList.namespaces }}</span>
                        <span style="font-size:20px">个</span>
                    </div>
                </el-card>
            </el-col>

            <el-col :span="6">
                <el-card class="card" :loading="dashLoading" :hoverable="true" style="background-color: rebeccapurple;">
                    <div class="ant-statistic-title" style="font-size:20px" align="center">Deployments</div>
                    <div class="ant-statistic-content" align="center">
                        <span style="font-size:40px">{{ dataList.deployments }}</span>
                        <span style="font-size:20px">个</span>
                    </div>
                </el-card>
            </el-col>

            <el-col :span="6">
                <el-card class="card" :loading="dashLoading" :hoverable="true" style="background-color: chocolate">
                    <div class="ant-statistic-title" style="font-size:20px" align="center">Pods</div>
                    <div class="ant-statistic-content" align="center">
                        <span style="font-size:40px">{{ dataList.pods }}</span>
                        <span style="font-size:20px">个</span>
                    </div>
                </el-card>
            </el-col>

            <el-col :span="6">
                <el-card class="card" :loading="dashLoading" :hoverable="true" style="background-color: rgb(25,187,80);">
                    <div class="ant-statistic-title" style="font-size:20px" align="center">Domains</div>
                    <div class="ant-statistic-content" align="center">
                        <span style="font-size:40px">{{ dataList.domains }}</span>
                        <span style="font-size:20px">个</span>
                    </div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    // import echarts from 'echarts'
    import {getDashbord} from '../../api/api'

    export default {
        data() {
            return {
                dashLoading: false,
                serverCount: 10,
                dataList: '',
            }
        },

        created() {
          this.get_data()
        },
   
        methods: {
          get_data() {
            getDashbord()
              .then((res) => {
                this.dataList = res.data.data
                // console.log(res.data.data)
            })
          },
        }
    }
</script>

<style scoped>
    .chart-container {
        width: 100%;
        float: left;
    }
    .card {
        height: 120px;
        /* width: 300px; */
        border-radius:8px;
        color: white;
    }
    
    .el-col {
        padding: 30px 20px;
    }
</style>
