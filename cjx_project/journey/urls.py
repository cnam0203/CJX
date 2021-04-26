from django.urls import path
from . import views

urlpatterns = [
    path('create-mapping-file', views.createMappingFile),
    path('upload-mapping-file', views.uploadMappingFile),
    path('import-touchpoint', views.importTouchpoint),
    path('export-touchpoint', views.exportTouchpoint),
    path('upload-touchpoint', views.uploadTouchpoint),
    path('read-instruction/<datasrc>', views.readDataSrcInstruction),
    path('read-instruction', views.readInstruction),
]