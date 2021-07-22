from django.urls import path
from . import views

urlpatterns = [
    path('get-visualize-graph-page', views.get_visualize_graph_page),
    path('get-process-graph', views.get_customer_process_discovery),
    path('get-cluster-journey-page', views.get_cluster_journey_page),
    path('get-cluster-journey', views.get_trace_clustering),
    path('get-decision-graph', views.get_decision_graph),
    path('get-cluster-user-page/<int:id>', views.get_cluster_user_page),
    path('get-cluster-user/<int:id>', views.get_cluster_user),
    path('analytics/visualize-process-graph', views.visualize_process_graph),
    path('analytics/trace-clustering', views.trace_clustering),
    path('analytics/decision-mining', views.decision_mining),
    path('analytics/cluster-customer/<int:id>', views.cluster_customer),
    path('table/<tablename>', views.get_list_data),
    path('form/update/<tablename>/<id>', views.update_form_data)
]