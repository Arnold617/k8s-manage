import axios from 'axios';

let base = 'http://127.0.0.1:8000';

export const requestLogin = params => { return axios.post(`${base}/login/`, params).then(res => res.data); };

// token
export const getTokenList = params => { return axios.get(`${base}/tokenList/`, { params: params });};

export const deleteTokenList = params => { return axios.delete(`${base}/tokenDetail/` + params.id );};

export const addTokenList = params => { return axios.post(`${base}/tokenList/`, params );};

export const updateTokenList = params => { return axios.patch(`${base}/tokenDetail/` + params.id, params );};

// namespace
export const getNameSpaces = params => { return axios.get(`${base}/NameSpaces/`) };
//dashbord
export const getDashbord = params => { return axios.get(`${base}/DashBord/`) };

// pod list
export const getPodList = params => { return axios.get(`${base}/PodList/`, { params: params }) };

// service list
export const getServiceList = params => { return axios.get(`${base}/ServiceList/`, { params: params }) };

// app 
export const getAppList = params => { return axios.get(`${base}/AppList/`, {params: params}) };

export const deleteApp = params => { return axios.delete(`${base}/AppDetail/` + params.id) };

export const addApp = params => { return axios.post(`${base}/AppList/`, params) };

export const updateApp = params => { return axios.patch(`${base}/AppDetail/` + params.id, params) };

// deployment
export const getDeploymentList = params => { return axios.get(`${base}/DeploymentList/`, {params: params}) };

export const deleteDeployment = params => { return axios.delete(`${base}/DeploymentDetail/` + params.id, {"data":{id: params.id}}) };

export const addDeployment = params => { return axios.post(`${base}/DeploymentList/`, params) };

export const updateDeployment = params => { return axios.patch(`${base}/DeploymentDetail/` + params.id, params) };

// cronjob
export const getCronJobList = params => { return axios.get(`${base}/CronJobList/`, {params: params}) };

export const deleteCronJob = params => { return axios.delete(`${base}/CronJobDetail/` + params.id, {"data":{id: params.id}}) };

export const addCronJob = params => { return axios.post(`${base}/CronJobList/`, params) };

export const updateCronJob = params => { return axios.patch(`${base}/CronJobDetail/` + params.id, params) };

// ingress
export const getIngressList = params => { return axios.get(`${base}/IngressList/`, {params: params}) };

export const deleteIngress = params => { return axios.delete(`${base}/IngressDetail/` + params.id, {"data":{id: params.id}}) };

export const addIngress = params => { return axios.post(`${base}/IngressList/`, params) };

export const updateIngress = params => { return axios.patch(`${base}/IngressDetail/` + params.id, params) };
