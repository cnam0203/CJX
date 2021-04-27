from django.urls import path
from . import views

urlpatterns = [
    path('create-mapping-file', views.create_mapping_file),
    path('upload-mapping-file', views.upload_mapping_file),
    path('import-touchpoint', views.import_touchpoint),
    path('export-touchpoint', views.export_touchpoint),
    path('upload-touchpoint', views.upload_touchpoint),
    path('read-instruction/<datasrc>', views.read_detail_instruction),
    path('read-instruction', views.read_instruction),
]