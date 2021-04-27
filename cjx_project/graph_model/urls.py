from django.urls import path
from . import views

urlpatterns = [
    path('get-visualize-graph-page', views.get_visualize_graph_page),
    path('get-process-graph', views.get_process_graph),
    path('get-cluster-journey-page', views.get_cluster_journey_page),
    path('get-cluster-journey', views.get_cluster_journey),
    path('get-cluster-user-page/<int:id>', views.get_cluster_user_page),
    path('get-cluster-user/<int:id>', views.get_cluster_user)
]