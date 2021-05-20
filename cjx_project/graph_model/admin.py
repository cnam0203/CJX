from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils.translation import gettext, gettext_lazy as _

from .models import Journey_Cluster_Model
from .models import Journey_Process_Graph
from .models import Clustered_Journey_Graph
from .models import Clustered_Customer
# Register your models here.

class Journey_Process_Graph_Admin(admin.ModelAdmin):
    search_fields = ("id", "startDate", "endDate", "runDate", "type")
    list_display = ("id", "startDate", "endDate",
                    "runDate", "type", "image")

    def image(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.link)
    image.allow_tags = True

class Clustered_Journey_Graph_Admin(admin.ModelAdmin):
    search_fields = ("id", "clusterID", "type", "clusterName")
    list_display = ("id", "cluster_link", "clusterNumber",
                    "clusterName", "type", "image")

    def cluster_link(self, obj):
        link = "/admin/graph_models/journey_cluster_model/" + str(obj.clusterID)
        return format_html("<a href='{}'>{}</a>", link, obj.clusterID)

    def image(self, obj):
        if (obj.link != ''):
            return format_html("<a href='{url}'>{url}</a>", url=obj.link)
        else:
            return ''
    image.allow_tags = True

class Journey_Cluster_Model_Admin(admin.ModelAdmin):
    search_fields = ("startDate", "endDate", "runDate",
                     "algorithm", "preprocessing", "numberClusters")
    list_display = ("id", "runDate", "algorithm", "preprocessing",
                    "numberClusters", "accuracy", "cluster_now")

    def cluster_now(self, obj):
        link = "/admin/graph_model/get-cluster-user-page/" + str(obj.id)
        return format_html("<a href='{}'>{}</a>", link, "Cluster Now")


class Clustered_Customer_Admin(admin.ModelAdmin):
    list_display = ("customer", "clusterDate", "cluster_link", "fromDate",
                    "toDate", "journey", "clusterName", "cluster_graph_link")
    search_fields = ("clusterDate", "cluster__clusterName")

    def customer(self, obj):
        link = "/admin/company_items/customer/" + str(obj.customer_id)
        return format_html("<a href='{}'>{}</a>", link, obj.customer_id)

    def cluster_link(self, obj):
        link = "/admin/graph_model/journey_cluster_model/" + str(obj.cluster.clusterID)
        return format_html("<a href='{}'>{}</a>", link, obj.cluster.clusterID)

    def clusterName(self, obj):
        return obj.cluster.clusterName

    def cluster_graph_link(self, obj):
        return format_html("<a href='{}'>{}</a>", obj.cluster.link, obj.cluster.link)

admin.site.register(Journey_Cluster_Model, Journey_Cluster_Model_Admin)
admin.site.register(Journey_Process_Graph, Journey_Process_Graph_Admin)
admin.site.register(Clustered_Journey_Graph, Clustered_Journey_Graph_Admin)
admin.site.register(Clustered_Customer, Clustered_Customer_Admin)