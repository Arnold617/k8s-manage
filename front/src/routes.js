import Login from './views/Login.vue'
import NotFound from './views/404.vue'
import Home from './views/Home.vue'
import dashbord from './views/dashbord/index.vue'
import auth from './views/auth/index.vue'
import appManage from './views/appManage/index.vue'
import logs from './views/logs/index.vue'
import apiManage from './views/apiManage/index.vue'
import appDetail from './views/appManage/appdetail.vue'
import podDetail from './views/appManage/podDetail.vue'
import cronjob from './views/appManage/cronjob.vue'
import ingress from './views/appManage/ingress.vue'


let routes = [
    {
        path: '/login',
        component: Login,
        name: '',
        hidden: true
    },
    {
        path: '/404',
        component: NotFound,
        name: '',
        hidden: true
    },
    {
        path: '/',
        component: Home,
        redirect: '/dashbord',
        name: '',
        iconCls: 'fa el-icon-share',
        leaf: true,//只有一个节点
        // hidden: true,  // 隐藏菜单栏
        children: [
            { path: '/dashbord', component: dashbord, name: 'Dashbord'}
        ]
    },
    {
        path: '/',
        component: Home,
        name: '',
        leaf: true,//只有一个节点
        hidden: true,  // 隐藏菜单栏
        children: [
            { path: '/appDetail', component: appDetail, name: 'appDetail'}
        ]
    },
    {
        path: '/',
        component: Home,
        name: '',
        leaf: true,//只有一个节点
        hidden: true,  // 隐藏菜单栏
        children: [
            { path: '/podDetail', component: podDetail, name: 'podDetail'}
        ]
    },
    {
        path: '/',
        component: Home,
        name: '应用管理',
        iconCls: 'fa el-icon-menu',//图标样式class
        // leaf: true,
        children: [
			{ path: '/deployments', component: appManage, name: 'Deployments'},
            { path: '/ingresses', component: ingress, name: 'Ingresses'},
			{ path: '/cronjobs', component: cronjob, name: 'CronJobs'},
        ]
    },
    // {
    //     path: '/',
    //     component: Home,
    //     name: '',
    //     iconCls: 'fa fa-id-card-o',
	// 	leaf: true,
    //     children: [
    //         { path: '/auth', component: auth, name: '权限管理' }
    //     ]
    // },
    {
        path: '/',
        component: Home,
        name: '',
        iconCls: 'fa el-icon-setting',
		leaf: true,
        children: [
            { path: '/apiManage', component: apiManage, name: '接口管理' }
        ]
    },
	{
	    path: '/',
	    component: Home,
	    name: '',
	    iconCls: 'fa el-icon-view',
	    leaf: true,//只有一个节点
	    children: [
	        { path: '/logs', component: logs, name: '日志审计' }
	    ]
	},
    {
        path: '*',
        hidden: true,
        redirect: { path: '/404' }
    }
];

export default routes;