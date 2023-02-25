## 管理Kubernetes资源 

### 通过此平台可以实现如下功能可以操作
* namespace 
* deployment
* service
* ingress
* pod (webshell)
* cronjob
* node 节点管理
* 权限根据namespace分配
* 日志审计

***

### 用到的技术
* Python3.+
* Django3.+
* Mysql5.6+
* Channels4.0+
* [Kuberneters-client](https://github.com/kubernetes-client/python)
* [Xterm4.+](https://github.com/xtermjs/xterm.js)
* [Vue-element](https://github.com/taylorchen709/vue-admin)
* [Vue-admin](https://element.eleme.cn/)

***

### 部署运行

* 前端 =>  [front](https://github.com/Arnold617/k8s-manage/tree/master/front)
* 后端 =>  [backend](https://github.com/Arnold617/k8s-manage/tree/master/backend)

***

### 功能界面
![image](https://github.com/Arnold617/k8s-manage/blob/master/images/k8s.gif)

#### 登陆
![image](https://github.com/Arnold617/k8s-manage/blob/master/images/login.png)

#### dashbord
![image](https://github.com/Arnold617/k8s-manage/blob/master/images/dashbord.png)

#### 应用
![image](https://github.com/Arnold617/k8s-manage/blob/master/images/app.png)

#### deployment
![image](https://github.com/Arnold617/k8s-manage/blob/master/images/deployment.png)

#### pod List
![image](https://github.com/Arnold617/k8s-manage/blob/master/images/pod.png)

#### webshell
![image](https://github.com/Arnold617/k8s-manage/blob/master/images/webshell.png)

#### node
![image](https://github.com/Arnold617/k8s-manage/blob/master/images/node.png)


### 待实现功能：
* 多集群配置
* 节点自动部署
* 环境变量应用
* 应用支持多集群环境配置
* 数据卷功能(PV)
