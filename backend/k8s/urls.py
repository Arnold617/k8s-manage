from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from app.view import login
from app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', login.Login.as_view(), name="login"),

    path('tokenList/', K8sTokenList.as_view(), name="token_list"),
    path('tokenDetail/<int:pk>', K8sTokenDetail.as_view(), name="token_detail"),

    path('NameSpaces/', NameSpaces.as_view(), name="nameSpaces"),
    path('PodList/', PodList.as_view(), name="pod list"),
    path('ServiceList/', ServiceList.as_view(), name="service list"),
    path('DashBord/', DataList.as_view(), name="k8s data"),

    path('AppList/', AppList.as_view(), name="app list"),
    path('AppDetail/<int:pk>', AppDetail.as_view(), name="app detail"),
    # deployment
    path('DeploymentList/', DeploymentList.as_view(), name="deployment list"),
    path('DeploymentDetail/<int:pk>', DeploymentDetail.as_view(), name="deployment detail"),

    # cronjob
    path('CronJobList/', CronJobList.as_view(), name="deployment list"),
    path('CronJobDetail/<int:pk>', CronJobDetail.as_view(), name="deployment detail"),

    # ingress
    path('IngressList/', IngressList.as_view(), name="deployment list"),
    path('IngressDetail/<int:pk>', IngressDetail.as_view(), name="deployment detail"),

]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
