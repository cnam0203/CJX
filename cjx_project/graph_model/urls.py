from django.urls import path
from . import views

urlpatterns = [
    path('get-visualize-graph-page', views.getVisualizeGraphPage),
    path('get-process-graph', views.getProcessGraph),
    path('get-cluster-journey-page', views.getClusterJourneyPage),
    path('get-cluster-journey', views.getClusterJourney),
    path('get-cluster-user-page/<int:id>', views.getClusterUserPage),
    path('get-cluster-user/<int:id>', views.getClusterUser)
]