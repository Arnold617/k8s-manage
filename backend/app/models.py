from django.db import models

# Create your models here.


class Deployment(models.Model):

    name = models.CharField(max_length=128)
    replicas = models.IntegerField()
    imageUrl = models.CharField(max_length=512)
    containerPort = models.IntegerField()
    nameSpace = models.CharField(max_length=128)
    projectName = models.CharField(max_length=256)
    env = models.CharField(max_length=256, null=True)
    cpuLimit = models.IntegerField()
    memoryLimit = models.IntegerField()


class CronJob(models.Model):
    name = models.CharField(max_length=128)
    env = models.CharField(max_length=256, null=True)
    command = models.CharField(max_length=256, null=True)
    schedule = models.CharField(max_length=128)
    imageUrl = models.CharField(max_length=256)
    namespace = models.CharField(max_length=128)
    cpuLimit = models.IntegerField()
    memoryLimit = models.IntegerField()
    # projectName = models.CharField(max_length=256)


class Ingress(models.Model):
    name = models.CharField(max_length=128)
    namespace = models.CharField(max_length=128)
    host = models.CharField(max_length=128)
    path = models.CharField(max_length=128)
    serverName = models.CharField(max_length=128)
    servicePort = models.CharField(max_length=16)


class appList(models.Model):
    projectName = models.CharField(max_length=256)
    imageUrl = models.CharField(max_length=512)
    nameSpace = models.CharField(max_length=128)

    class Meta:
        unique_together = ('projectName',)


class k8sToken(models.Model):
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=256)
    apiToken = models.CharField(max_length=4096)

