
from django.views import View
from django.http import JsonResponse
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import k8sToken, appList, Deployment, CronJob, Ingress
from .page import AppPageNumberPagination
import django_filters
from app.view.api import KubernetesTools



class K8sTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = k8sToken
        fields = '__all__'

class AppListSerializer(serializers.ModelSerializer):

    class Meta:
        model = appList
        fields = '__all__'

class DeploymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deployment
        fields = '__all__'


class CronJobSerializer(serializers.ModelSerializer):

    class Meta:
        model = CronJob
        fields = '__all__'


class IngressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingress
        fields = '__all__'


class AppListFilter(filters.FilterSet):

    projectName = django_filters.CharFilter(field_name="projectName", lookup_expr="icontains")
    nameSpace = django_filters.CharFilter(field_name="nameSpace", lookup_expr="icontains")

    class Meta:
        module = appList
        fields = ['projectName', 'nameSpace']


class DeploymentFilter(filters.FilterSet):

    nameSpace = django_filters.CharFilter(field_name="nameSpace", lookup_expr="icontains")
    projectName = django_filters.CharFilter(field_name="projectName", lookup_expr="icontains")
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        module = Deployment
        fields = ['nameSpace', 'projectName', 'name']


class CronJobFilter(filters.FilterSet):

    namespace = django_filters.CharFilter(field_name="namespace", lookup_expr="icontains")
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        module = CronJob
        fields = ['namespace', 'name']


class IngressFilter(filters.FilterSet):

    namespace = django_filters.CharFilter(field_name="namespace", lookup_expr="icontains")
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        module = Ingress
        fields = ['namespace', 'name']


class K8sTokenList(generics.ListCreateAPIView):
    queryset = k8sToken.objects.all().order_by('id')
    serializer_class = K8sTokenSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = AppPageNumberPagination


class K8sTokenDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = k8sToken.objects.all().order_by('id')
    serializer_class = K8sTokenSerializer


class AppList(generics.ListCreateAPIView):
    queryset = appList.objects.all().order_by('id')
    serializer_class = AppListSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = AppPageNumberPagination
    filter_class = AppListFilter


class AppDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = appList.objects.all().order_by('id')
    serializer_class = AppListSerializer


class DeploymentList(generics.ListCreateAPIView):
    queryset = Deployment.objects.all().order_by('id')
    serializer_class = DeploymentSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = AppPageNumberPagination
    filter_class = DeploymentFilter

    def create(self, request, *args, **kwargs):
        # print(request.data)
        data = request.data
        name = data.get('name')
        nameSpace = data.get('nameSpace')
        containerPort = data.get('containerPort')
        imageUrl = data.get('imageUrl')
        replicas = data.get('replicas')
        cpuLimit = data.get('cpuLimit')
        memoryLimit = data.get('memoryLimit')
        env = data.get('env')
        tools = KubernetesTools()
        body_data = tools.create_deployment_object(name, nameSpace, containerPort, imageUrl,
                                                         replicas, cpuLimit, memoryLimit)
        response_dep = tools.create_deployment(body_data, name, nameSpace)

        if response_dep is False:
            exit(0)

        response_svc = tools.create_service(name, containerPort, nameSpace)
        if response_svc is False:
            exit(0)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DeploymentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deployment.objects.all().order_by('id')
    serializer_class = DeploymentSerializer

    def destroy(self, request, *args, **kwargs):
        id = request.data.get('id')
        data = Deployment.objects.filter(id=id).order_by()

        for info in data:
            tools = KubernetesTools()
            response_dep = tools.delete_deployment(info.name, info.nameSpace)

            response_svc = tools.delete_service(info.name, info.nameSpace)

            # print(response_dep, response_svc)
            if response_dep and response_svc is True:
                print('ok,logs(delete success!)')
            else:
                print(response_dep, response_svc)
                exit(0)

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        data = request.data
        # print(data)

        tools = KubernetesTools()
        response = tools.update_deployment(data)
        if response is False:
            exit(0)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class CronJobList(generics.ListCreateAPIView):
    queryset = CronJob.objects.all().order_by('id')
    serializer_class = CronJobSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = AppPageNumberPagination
    filter_class = CronJobFilter

    def create(self, request, *args, **kwargs):
        # print(request.data)
        data = request.data
        name = data.get('name')
        namespace = data.get('namespace')
        command = data.get('command')
        imageUrl = data.get('imageUrl')
        schedule = data.get('schedule')
        cpuLimit = data.get('cpuLimit')
        memoryLimit = data.get('memoryLimit')
        env = data.get('env')
        tools = KubernetesTools()
        body = tools.create_cron_job_object(name, namespace, imageUrl, command, schedule, cpuLimit, memoryLimit)
        response_dep = tools.create_cron_job(name, namespace, body)
        if response_dep is False:
            exit(0)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CronJobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CronJob.objects.all().order_by('id')
    serializer_class = CronJobSerializer

    def destroy(self, request, *args, **kwargs):
        id = request.data.get('id')
        data = CronJob.objects.filter(id=id).order_by()

        for info in data:
            tools = KubernetesTools()
            response_dep = tools.delete_cron_job(info.name, info.namespace)

            # print(response_dep, response_svc)
            if response_dep is True:
                print('ok,logs(CronJob delete success!)')
            else:
                print(response_dep)
                exit(0)

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name')
        namespace = data.get('namespace')
        command = data.get('command')
        imageUrl = data.get('imageUrl')
        schedule = data.get('schedule')
        cpuLimit = data.get('cpuLimit')
        memoryLimit = data.get('memoryLimit')
        env = data.get('env')
        tools = KubernetesTools()
        body = tools.create_cron_job_object(name, namespace, imageUrl, command, schedule, cpuLimit, memoryLimit)
        response = tools.update_cron_job(name, namespace, body)
        if response is False:
            exit(0)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class IngressList(generics.ListCreateAPIView):
    queryset = Ingress.objects.all().order_by('id')
    serializer_class = IngressSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = AppPageNumberPagination
    filter_class = IngressFilter

    def create(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name')
        namespace = data.get('namespace')
        host = data.get('host')
        path = data.get('path')
        service_name = data.get('serviceName')
        service_port = int(data.get('servicePort'))

        tools = KubernetesTools()
        body = tools.create_ingress_object(name, namespace, host, path, service_name, service_port)
        response = tools.create_ingress(name, namespace, body)
        if response is False:
            exit(0)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class IngressDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingress.objects.all().order_by('id')
    serializer_class = IngressSerializer

    def destroy(self, request, *args, **kwargs):
        id = request.data.get('id')
        data = Ingress.objects.filter(id=id).order_by()

        for info in data:
            tools = KubernetesTools()
            response_dep = tools.delete_ingress(info.name, info.namespace)

            if response_dep is True:
                print('ok,logs(CronJob delete success!)')
            else:
                print(response_dep)
                exit(0)

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name')
        namespace = data.get('namespace')
        host = data.get('host')
        path = data.get('path')
        service_name = data.get('serviceName')
        service_port = data.get('servicePort')

        tools = KubernetesTools()
        body = tools.create_ingress_object(name, namespace, host, path, service_name, service_port)
        response = tools.update_ingress(name, namespace, body)
        if response is False:
            exit(0)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class NameSpaces(View):

    def get(self, request):
        tools = KubernetesTools()
        namespace_list = tools.get_namespace_list()
        data = {'namespace_list': namespace_list}
        return JsonResponse(data)


class PodList(View):

    def get(self, request):
        namespace = request.GET.get('namespace')
        name = request.GET.get('name')
        tools = KubernetesTools()
        result = tools.list_pod(namespace, name)
        data = {"data": result}
        return JsonResponse(data)


class ServiceList(View):

    def get(self, request):
        namespace = request.GET.get('namespace')
        tools = KubernetesTools()
        result = tools.get_services(namespace)
        data = {"data": result}
        return JsonResponse(data)


class DataList(View):

    def get(self, request):
        tools = KubernetesTools()
        result = tools.get_k8s_data()
        data = {"data": result}
        return JsonResponse(data)
