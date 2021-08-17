from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils.translation import gettext, gettext_lazy as _

from .models import Touchpoint
from .models import Channel_Type
from .models import Device_Browser
from .models import Device_OS
from .models import Device_Category
from .models import Interact_Item_Type
from .models import Experience_Emotion
from .models import Traffic_Source_Type
from .models import Action_Type
from .models import Journey_Customer
from .models import Matching_Column
from .models import Matching_Report
from .models import Data_Source
from .models import Import_File_Log
from .models import Data_Source_Permission


# Register your models here.
class TouchpointAdmin(admin.ModelAdmin):
    search_fields = ("action_type", "channel_type",
                     "customer_id", "device_category")
    list_display = ("id", "customer", "time", "geo_continent", "geo_country", "action_type",
                    "channel_type", "device_category", "traffic_source_name", "interact_item", "experience_emotion")

    def interact_item(self, obj):
        if (obj.interact_item_type and obj.interact_item_id):
            link = "/admin/company_items/" + obj.interact_item_type.name + "/" + str(obj.interact_item_id)
            return format_html("<a href='{}'>{}</a>", link, obj.interact_item_type)
        else:
            return 'None'

    def customer(self, obj):
        customerID = Journey_Customer.objects.get(customerID=obj.customer_id)
        link = "/admin/journey/journey_customer/" + str(customerID.id)
        return format_html("<a href='{}'>{}</a>", link, str(obj.customer_id))


class Source_Type_Admin(admin.ModelAdmin):
    list_display = ("id", "name")

class Device_Browser_Admin(admin.ModelAdmin):
    list_display = ("id", "name")

class Device_OS_Admin(admin.ModelAdmin):
    list_display = ("id", "name")

class Device_Category_Admin(admin.ModelAdmin):
    list_display = ("id", "name")

class Interact_Item_Type_Admin(admin.ModelAdmin):
    list_display = ("id", "name")

class Experience_Emotion_Admin(admin.ModelAdmin):
    list_display = ("id", "name")

class Journey_Customer_Admin(admin.ModelAdmin):
    list_display = ("id", "customerID", "register_date")

class Data_Source_Admin(admin.ModelAdmin):
    list_display = ("id", "name", "created_date", "staff_create", "last_update", "is_public")
    fields = ["name", "is_public"]
    

class Import_File_Log_Admin(admin.ModelAdmin):
    list_display = ("id", "import_date", "number_rows", "staff")

class Matching_Report_Admin(admin.ModelAdmin):
    list_display = ("id", "name", "instruction")

    def instruction(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.instruction_link)

class Matching_Column_Admin(admin.ModelAdmin):
    list_display = ("id", "report", "journey_column", "report_column", "function")
    search_fields = ("report__name", "journey_column", "report_column")

class Channel_Type_Admin(admin.ModelAdmin):
    list_display = ("id", "name")

class Action_Type_Admin(admin.ModelAdmin):
    list_display = ("id", "name")


class Data_Source_Permission_Admin(admin.ModelAdmin):
    list_display = ("id", "data_source", "user")

admin.site.register(Data_Source_Permission, Data_Source_Permission_Admin)
admin.site.register(Touchpoint, TouchpointAdmin)
admin.site.register(Channel_Type, Channel_Type_Admin)
admin.site.register(Action_Type, Action_Type_Admin)
admin.site.register(Traffic_Source_Type, Source_Type_Admin)
admin.site.register(Device_Browser, Device_Browser_Admin)
admin.site.register(Device_Category, Device_Category_Admin)
admin.site.register(Device_OS, Device_OS_Admin)
admin.site.register(Interact_Item_Type, Interact_Item_Type_Admin)
admin.site.register(Experience_Emotion, Experience_Emotion_Admin)
admin.site.register(Journey_Customer, Journey_Customer_Admin)
admin.site.register(Matching_Column, Matching_Column_Admin)
admin.site.register(Matching_Report, Matching_Report_Admin)
admin.site.register(Data_Source, Data_Source_Admin)
admin.site.register(Import_File_Log, Import_File_Log_Admin)
