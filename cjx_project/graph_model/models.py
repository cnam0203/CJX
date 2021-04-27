from django.db import models

# Create your models here.


class Journey_Cluster_Model(models.Model):
    id = models.AutoField(primary_key=True)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    numberClusters = models.IntegerField(blank=True, null=True)
    algorithm = models.CharField(max_length=50, blank=True, null=True)
    preprocessing = models.CharField(max_length=50, blank=True, null=True)
    accuracy = models.FloatField(blank=True, null=True)
    preprocessingModelFile = models.CharField(
        max_length=150, blank=True, null=True)
    clusterModelFile = models.CharField(max_length=150, blank=True, null=True)
    runDate = models.DateTimeField(auto_now=True)


class Clustered_Journey_Graph(models.Model):
    id = models.AutoField(primary_key=True)
    clusterID = models.IntegerField(blank=True, null=True)
    clusterNumber = models.IntegerField(blank=True, null=True)
    clusterName = models.CharField(
        max_length=50, blank=True, default="undefined", null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    link = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return (str(self.clusterID) + '-' + str(self.clusterNumber) + '-' + (self.clusterName or '') + '-' + self.type)


class Journey_Process_Graph(models.Model):
    id = models.AutoField(primary_key=True)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    runDate = models.DateTimeField()
    type = models.CharField(max_length=50, blank=True, null=True)
    link = models.CharField(max_length=150, blank=True, null=True)


class Clustered_Customer(models.Model):
    customer_id = models.BigIntegerField(blank=True, null=True)
    clusterDate = models.DateTimeField(auto_now=True)
    fromDate = models.DateField()
    toDate = models.DateField()
    journey = models.JSONField()
    cluster = models.ForeignKey(
        Clustered_Journey_Graph, null=True, on_delete=models.SET_NULL)
