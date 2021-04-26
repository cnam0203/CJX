"""cjx_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.contrib.staticfiles.urls import static
from django.conf import settings

admin.site.site_header = 'Organization Administration'                      # default: "Django Administration"
admin.site.index_title = 'Customer Journey Management'                      # default: "Site administration"
admin.site.site_title = 'Customer Journey Management'                       # default: "Django site admin"

urlpatterns = [
    path('admin/journey/', include('journey.urls')),
    path('admin/graph_model/', include('graph_model.urls')),
    path('admin/company_items/', include('company_items.urls')),
    path('admin/', admin.site.urls),
    path('', admin.site.urls)
]

urlpatterns += static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT)