from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_page),
    path('logout', views.logout_page)
]