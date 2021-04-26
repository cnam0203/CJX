from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _

from .models import API_KEY

# Register your models here.
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'groups'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    def has_change_permission(self, request, obj=None):
        if obj is None:
           return True
        else:
            if request.user == obj:
                return False
            
            isAdminRequest = request.user.groups.filter(name="admin").exists()
            isAdminUser = obj.groups.filter(name="admin").exists()
            isSuperUserRequest = request.user.is_superuser
            isSuperUser = obj.is_superuser

            if isSuperUserRequest:
                if isSuperUser:
                    return False
                else:
                    return True
            if isAdminRequest:
                if isSuperUser:
                    return False
                elif isAdminUser:
                    return False
                else:
                    return True
            else:
                return False

    def has_delete_permission(self, request, obj=None):
        if obj is None:
           return True
        else:
            if request.user == obj:
                return False
            
            isAdminRequest = request.user.groups.filter(name="admin").exists()
            isAdminUser = obj.groups.filter(name="admin").exists()
            isSuperUserRequest = request.user.is_superuser
            isSuperUser = obj.is_superuser
            if isSuperUserRequest:
                if isSuperUser:
                    return False
                else:
                    return True
            if isAdminRequest:
                if isSuperUser:
                    return False
                elif isAdminUser:
                    return False
                else:
                    return True
            else:
                return False


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(API_KEY)