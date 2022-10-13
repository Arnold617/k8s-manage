
import urllib3,json
from app.models import k8sToken
from kubernetes import client
from django.http import JsonResponse
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream


# 解决"verified HTTPS request is being made to host"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def k8s_token():
    result = k8sToken.objects.filter(id=1).order_by('id')
    return result[0]


class KubernetesTools(object):

    def __init__(self):
        info = k8s_token()
        configuration = client.Configuration()
        setattr(configuration, 'verify_ssl', False)
        client.Configuration.set_default(configuration)
        configuration.host = info.url
        configuration.verify_ssl = False
        configuration.debug = False
        configuration.api_key = {"authorization": "Bearer " + info.apiToken}
        client.Configuration.set_default(configuration)
        self.core_api_v1 = client.CoreV1Api(client.ApiClient(configuration))
        self.apps_v1_api = client.AppsV1Api(client.ApiClient(configuration))
        self.batch_v1_api = client.BatchV1beta1Api(client.ApiClient(configuration))
        self.networking_v1_api = client.NetworkingV1beta1Api(client.ApiClient(configuration))


    def get_namespace_list(self):
        namespace_list = []
        for ns in self.core_api_v1.list_namespace().items:
            namespace_list.append(ns.metadata.name)

        return namespace_list


    def create_namespace(self, namespace="default"):

        list_names = self.get_namespace_list()
        if namespace not in list_names:
            body = {'apiVersion': 'v1', 'kind': 'Namespace',
                    'metadata': {'name': namespace, 'labels': {'name': namespace}}}
            try:
                self.core_api_v1.create_namespace(body)
            except ApiException as e:
                return e
        else:
            return JsonResponse("已经存在namespace:{%s}" % namespace)


    def get_services(self, namespace):
        service_list = []
        if namespace:
            response = self.core_api_v1.list_namespaced_service(namespace)
            for info in response.items:
                service_list.append({'name':info.metadata.name, 'port': info.spec.ports[0].port})
        else:
            response = self.core_api_v1.list_service_for_all_namespaces()
            for info in response.items:
                service_list.append({'name': info.metadata.name, 'port': info.spec.ports[0].port})

        return service_list
            # print("%s \t%s \t%s \t%s \t%s \n" % (
            #     i.kind, i.metadata.namespace, i.metadata.name, i.spec.cluster_ip, i.spec.ports))


    def get_pod_info(self,namespaces,pod_name):

        resp = self.core_api_v1.read_namespaced_pod(namespace=namespaces,name=pod_name)
        return resp


    def list_pod(self, namespace, deployment_name):

        if namespace and deployment_name:
            try:
                api_response = self.core_api_v1.list_namespaced_pod(
                    namespace = namespace,
                    label_selector="app=%s" % deployment_name
                )
                data = []
                for pod in api_response.items:
                    # if pod.metadata.labels['app'] == deployment_name:
                    data.append({
                        "name": pod.metadata.name,
                        "ip": pod.status.pod_ip,
                        "node": pod.status.host_ip,
                        "status": pod.status.phase,
                        "startTime": pod.status.start_time,
                    })
                return data
            except ApiException as e:
                return False

    def list_deployment(self, namespace):

        list_temp = []
        api_response = self.apps_v1_api.list_namespaced_deployment(namespace)

        for info in api_response.items:
            list_temp.append(info.metadata.name)
        return list_temp


    def delete_deployment(self, deployment_name, namespace):

        if deployment_name in self.list_deployment(namespace):
            try:
                resp = self.apps_v1_api.delete_namespaced_deployment(
                    name=deployment_name,
                    namespace=namespace,

                    body=client.V1DeleteOptions(
                        propagation_policy="Foreground",
                        grace_period_seconds=10
                    ),
                )
                if resp:
                    return True
            except ApiException as e:
                return False


    def create_deployment(self, deployment_body, deployment_name, namespace):
        print("create_deployment")

        if deployment_name not in self.list_deployment(namespace):

            try:
                response = self.apps_v1_api.create_namespaced_deployment(
                    namespace=namespace,
                    body=deployment_body
                )
                # print(response)
                if response:
                    return True

            except ApiException as e:
                return False

        else:
            return False


    # 获取pod 日志
    def get_pod_logs(self,namespaces,pod_name):
        """
        pretty美化输出
        tail_lines=200输出最近200行
        """
        log_content = self.core_api_v1.read_namespaced_pod_log(pod_name, namespaces, pretty=True, tail_lines=200)
        return log_content


    def get_list_node(self):

        api_response = self.core_api_v1.list_node()
        data = {}
        for node in api_response.items:
            data[node.metadata.name] = {"name": node.metadata.name,
                                    "status": node.status.conditions[-1].type if node.status.conditions[-1].status == "True" else "NotReady",
                                    "ip": node.status.addresses[0].address,
                                    "kubelet_version": node.status.node_info.kubelet_version,
                                    "os_image": node.status.node_info.os_image,
                                     }
        return json.dumps(data)


    def create_deployment_object(self, deployment_name, namespace, container_port, container_image, replicas, cpu, memory):
        print("create_deployment_obj")
        container = client.V1Container(
            name=deployment_name,
            image=container_image,
            ports=[client.V1ContainerPort(container_port=container_port)],
            resources=client.V1ResourceRequirements(requests={"cpu": str(cpu) + "m", "memory": str(memory) + "Mi"},
                                                    limits={"cpu": str(cpu) + "m", "memory": str(memory) + "Mi"}))

        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": deployment_name}),
            spec=client.V1PodSpec(containers=[container]),
        )
        spec = client.V1DeploymentSpec(
            replicas=replicas,
            selector={"matchLabels": {"app": deployment_name}, "namespace": namespace},
            template=template
        )
        deployment_temp = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(name=deployment_name),
            spec=spec,
        )
        return deployment_temp


    def update_deployment(self, data):

        name = data.get('name')
        namespace = data.get('nameSpace')
        containerPort = data.get('containerPort')
        imageUrl = data.get('imageUrl')
        replicas = data.get('replicas')
        cpuLimit = data.get('cpuLimit')
        memoryLimit = data.get('memoryLimit')
        env = data.get('env')

        body = self.create_deployment_object(
            deployment_name=name,
            namespace=namespace,
            container_port=containerPort,
            container_image=imageUrl,
            replicas=replicas,
            cpu=cpuLimit,
            memory=memoryLimit
        )

        try:
            response = self.apps_v1_api.patch_namespaced_deployment(name, namespace, body)
            # print(response.status.conditions[0].status)
            if response:
                return True
            return False

        except ApiException as e:
            return False


    def create_service(self, deployment_name, container_port, namespace):
        body = {'apiVersion': 'v1', 'kind': 'Service',
                'metadata': {'name': deployment_name, 'labels': {'app': deployment_name}},
                'spec': {'ports': [{'port': container_port, 'targetPort': container_port}],
                         'selector': {'app': deployment_name}}
                }
        try:
            response = self.core_api_v1.create_namespaced_service(
                namespace=namespace,
                body=body
            )
            if response:
                return True

        except ApiException as e:
            return False


    def delete_service(self, service_name, namespace):

        try:
            response = self.core_api_v1.delete_namespaced_service(
                name=service_name,
                namespace=namespace,
                body=client.V1DeleteOptions(
                    propagation_policy="Foreground",
                    grace_period_seconds=15
                )
            )
            if response:
                return True

        except ApiException as e:
            return False


    def pod_exec(self, name, namespace, container=""):

        exec_command = [
            "/bin/sh",
            "-c",
            'TERM=xterm-256color; export TERM; [ -x /bin/bash ] '
            '&& ([ -x /usr/bin/script ] '
            '&& /usr/bin/script -q -c "/bin/bash" /dev/null || exec /bin/bash) '
            '|| exec /bin/sh']

        cont_stream = stream(self.core_api_v1.connect_get_namespaced_pod_exec,
                             name=name,
                             namespace=namespace,
                             container=container,
                             command=exec_command,
                             stderr=True, stdin=True,
                             stdout=True, tty=True,
                             _preload_content=False
                             )

        return cont_stream

    def judge_crontab_exists(self, namespace, name):
        cron_job_list = self.get_cronjob_list(namespace)
        for cron_job in cron_job_list:
            # print(cron_job.metadata.name)
            if name == cron_job.metadata.name:
                return True
        return False

    def get_cronjob_list(self, namespace):
        response = self.batch_v1_api.list_namespaced_cron_job(namespace)
        # print(type(response), response.items)
        return response.items

    def create_cron_job_object(self, name,namespace, image, command, schedule, cpu, memory ):

        container = client.V1Container(
            name=name,
            image=image,
            command=[command],
            resources=client.V1ResourceRequirements(requests={"cpu": str(cpu) + "m", "memory": str(memory) + "Mi"},
                                                    limits={"cpu": str(cpu) + "m", "memory": str(memory) + "Mi"}))
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": name}),
            spec=client.V1PodSpec(restart_policy="Never", containers=[container]))
        spec = client.V1JobSpec(
            template=template,
            backoff_limit=3)

        job = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(name=name),
            spec=spec)

        body = client.V1beta1CronJob(
                    api_version='batch/v1beta1',
                    kind='CronJob',
                    metadata=client.V1ObjectMeta(name=name),
                    spec=client.V1beta1CronJobSpec(
                        schedule=schedule,
                        successful_jobs_history_limit=3,
                        failed_jobs_history_limit=2,
                        job_template=job))
        return body

    def create_cron_job(self, name, namespace, body):
        if self.judge_crontab_exists(namespace, name):
            exit(0)
        else:
            try:
                api_response = self.batch_v1_api.create_namespaced_cron_job(
                    body=body,
                    namespace=namespace)

                if api_response:
                    return True
            except ApiException as e:
                return False

    def update_cron_job(self, name, namespace, body):
        try:
            response = self.batch_v1_api.patch_namespaced_cron_job(name, namespace, body)

            if response:
                return True
            return False

        except ApiException as e:
            return False

    def delete_cron_job(self, name, namespace):

        if self.judge_crontab_exists(namespace, name):
            try:
                resp = self.batch_v1_api.delete_namespaced_cron_job(
                    name=name,
                    namespace=namespace,
                    body=client.V1DeleteOptions(
                        propagation_policy="Foreground",
                        grace_period_seconds=10))

                if resp:
                    return True
            except ApiException as e:
                return False

    def create_ingress_object(self, name, namespace, host, path, svc_name, svc_port):

        body = client.NetworkingV1beta1Ingress(
            api_version="networking.k8s.io/v1beta1",
            # api_version="extensions/v1beta1",
            kind="Ingress",
            metadata=client.V1ObjectMeta(name=name, annotations={
                "nginx.ingress.kubernetes.io/rewrite-target": "/"
            }),
            spec=client.NetworkingV1beta1IngressSpec(
                rules=[client.NetworkingV1beta1IngressRule(
                    host=host,
                    http=client.NetworkingV1beta1HTTPIngressRuleValue(
                        paths=[client.NetworkingV1beta1HTTPIngressPath(
                            path=path,
                            backend=client.NetworkingV1beta1IngressBackend(
                                service_port=svc_port,
                                service_name=svc_name)
                            )
                        ]
                    )
                )]
            )
        )
        return body

    def create_ingress(self, name, namespace, body):
        if self.judge_ingress_exists(namespace, name):
            exit(0)
        try:
            resp = self.networking_v1_api.create_namespaced_ingress(
                                namespace=namespace, body=body)
            if resp:
                return True
        except ApiException as e:
            return False

    def update_ingress(self, name, namespace, body):

        if self.judge_ingress_exists(namespace, name):
            try:
                resp = self.networking_v1_api.patch_namespaced_ingress(name, namespace, body)
                if resp:
                    return True
            except ApiException as e:
                return False

    def delete_ingress(self, name, namespace):

        if self.judge_ingress_exists(namespace, name):
            try:
                resp = self.networking_v1_api.delete_namespaced_ingress(
                                name=name, namespace=namespace)
                if resp:
                    return True
            except ApiException as e:
                return False

    def judge_ingress_exists(self, namespace, name):

        ingress_list = self.networking_v1_api.list_namespaced_ingress(namespace)

        for ing in ingress_list.items:
            if name == ing.metadata.name:
                return True
        return False


