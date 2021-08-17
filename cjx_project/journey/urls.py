from django.urls import path
from . import views

urlpatterns = [
    path('create-mapping-file', views.create_mapping_file),
    path('upload-mapping-file', views.upload_mapping_file),
    path('import-touchpoint', views.import_touchpoint),
    path('import-csv-file', views.import_csv_file),
    path('read-instruction/<datasrc>', views.read_detail_instruction),
    path('read-instruction', views.read_instruction),
    path('report', views.report),
    path('change-password', views.change_password),
    path('documentation', views.documentation),
    path('documentation/<name>', views.detail_documentation),
    path('home', views.home),
    path('table/<tablename>', views.get_list_data),
    path('table/<tablename>/', views.get_list_data),
    path('form/create/<tablename>', views.create_form_data),
    path('form/update/<tablename>/<id>', views.update_form_data),
    path('form/delete/<tablename>/<id>', views.delete_form_data),
    path('import/upload-file', views.get_import_page),
    path('import/create-mapping-file', views.get_create_mapping_file),
    path('import/review-mapping-file', views.review_mapping_file),
    path('import/review-mapping-file/<reportId>', views.review_mapping_file),
    path('import/import-touchpoint-api', views.import_touchpoint_api),
]