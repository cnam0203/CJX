from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.apps import apps
from django.db import Error, DataError, DatabaseError, IntegrityError
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geoip2 import GeoIP2
from django.db.models import Count

from .models import Touchpoint, Journey_Customer, Action_Type, Channel_Type, Traffic_Source_Type, Device_Browser, Device_OS, Device_Category, Device_Category, Interact_Item_Type, Experience_Emotion, Matching_Report, Matching_Column
from .forms import Touchpoint_Form, Journey_Customer_Form, Action_Type_Form, Channel_Type_Form, Source_Type_Form, Device_Browser_Form, Device_OS_Form, Device_Category_Form, Interact_Item_Type_Form, Experience_Emotion_Form, Matching_Report_Form, Matching_Column_Form

from utils.path_helper import get_static_path
from utils.copy_object import copy_object
from datetime import datetime
from datetime import date


import json
from json import dumps
import os

# Create your views here.

formData = {
    'touchpoint': Touchpoint_Form,
    'journey_customer': Journey_Customer_Form,
    'action_type': Action_Type_Form,
    'channel_type': Channel_Type_Form,
    'traffic_source_type': Source_Type_Form,
    'device_browser': Device_Browser_Form,
    'device_os': Device_OS_Form,
    'device_category': Device_Category_Form,
    'interact_item_type': Interact_Item_Type_Form,
    'experience_emotion': Experience_Emotion_Form,
    'matching_column': Matching_Column_Form,
    'matching_report': Matching_Report_Form
}


@login_required(login_url="/authentication/login")
def home(request):
    total_customer = len(Journey_Customer.objects.values('customerID').distinct())
    new_customer = len(Journey_Customer.objects.filter(register_date__year=date.today().year,
                                                        register_date__month=date.today().month,
                                                        register_date__day=date.today().day).values('customerID').distinct())
    activites = list(Touchpoint.objects.order_by('-time').values('customer_id', 'time', 'action_type__name', 'channel_type__name', 'device_category__name', 'experience_emotion')[:5])
    
    total_usage = len(Touchpoint.objects.all())

    device_category_usage = list(Touchpoint.objects.all().values('device_category__name').annotate(total=Count('device_category__name')))
    if (device_category_usage[0]['device_category__name'] == 'None' and device_category_usage[0]['total'] == 0):
        device_category_data = []
    else:
        device_category_data = [[device['device_category__name'],(device['total']/total_usage)*100] for device in device_category_usage]

    channel_type_usage = list(Touchpoint.objects.all().values('channel_type__name').annotate(total=Count('channel_type__name')))
    if (channel_type_usage[0]['channel_type__name'] == 'None' and channel_type_usage[0]['total'] == 0):
        channel_type_data = []
    else:
        channel_type_data = [{'name': channel['channel_type__name'], 'y': (channel['total']/total_usage)*100} for channel in channel_type_usage]

    event_usage = list(Touchpoint.objects.all().values('action_type__name').annotate(total=Count('action_type__name')))
    if (event_usage[0]['action_type__name'] == 'None' and event_usage[0]['total'] == 0):
        event_data = []
    else:
        event_data = [[event['action_type__name'],(event['total']/total_usage)*100] for event in event_usage]

    return render(request, "journey/home.html", {'activities': activites, 
                                'total_customer': total_customer, 
                                'new_customer': new_customer,
                                'device_category_data': dumps(device_category_data),
                                'channel_type_data': dumps(channel_type_data),
                                'event_data': dumps(event_data)
    })


@login_required(login_url="/authentication/login")
def get_import_page(request):
    all_fields = {}
    matching_reports = [report for report in Matching_Report.objects.all()]
    matched_columns = [{'report_name': column.report.name,
                        'report_column': column.report_column,
                        'journey_column': column.journey_column,
                        'function': column.function
                        } for column in Matching_Column.objects.all()]

    for field in Touchpoint._meta.get_fields():
        if (field.name != "id" and field.name != "record_time"):
            data_type = field.get_internal_type()
            converted_type = ""

            if (data_type == "BigIntegerField" or data_type == "IntegerField" or data_type == "FloatField"):
                converted_type = "numeric"
            elif (data_type == "DateTimeField" or data_type == "DataField"):
                converted_type = "date"
            else:
                converted_type = "string"

            all_fields[field.name] = converted_type
    return render(request, "journey/import.html", {"allFields": all_fields, "matchingReports": matching_reports, "matchedColumns": matched_columns})


@login_required(login_url="/authentication/login")
def get_create_mapping_file(request):
    fields = [field.name for field in Touchpoint._meta.get_fields(
    ) if field.name != 'id' and field.name != 'report_time']
    reports = [report.name for report in Matching_Report.objects.all()]

    return render(request, "journey/mapping-file.html", {
        'reports': reports,
        'fields': fields,
        'functions': ['lower', 'upper', 'string', 'int', 'float', 'datetime', 'date']
    })


@login_required(login_url="/authentication/login")
def review_mapping_file(request, dataSrcName=None):
    matching_reports = [report for report in Matching_Report.objects.all()]
    list_matching_fields = []
    instruction_img = None

    if (dataSrcName is not None):
        list_matching_fields = [[row.report_column, row.journey_column, row.function]
                          for row in Matching_Column.objects.filter(report__name=dataSrcName)]
        instruction_img = Matching_Report.objects.get(
            name=dataSrcName).instruction_link

    return render(request, "journey/review-mapping.html", {"dataSrcs": matching_reports, 
                                                            "dataSrcName": dataSrcName, 
                                                            "listMatchingFields": list_matching_fields,
                                                            "instructionImg": instruction_img})

@login_required(login_url="/authentication/login")
def get_list_data(request, tablename):
    Model = apps.get_model(app_label="journey", model_name=tablename)
    new_data = []
    headers = []

    if (tablename == 'touchpoint'):
        data = list(Model.objects.all().values('id', 'customer_id', 'action_type__name', 'time', 'channel_type__name',
                    'device_browser__name', 'device_os__name', 'device_category__name', 'geo_continent',
                    'geo_country', 'geo_city', 'interact_item_type__name', 'interact_item_content',
                    'experience_emotion__name'))
        headers = ['id', 'customer_id', 'action_type', 'time', 'channel_type',
                    'browser', 'os', 'device_category', 'geo_continent',
                    'geo_country', 'geo_city', 'interact_item_type', 'interact_item_content',
                    'experience']
        new_data = data
    elif (tablename == 'matching_report'):
        data = list(Model.objects.all().values())
        headers = ['id', 'name', 'instructionExample']

        for obj in data:
            obj['instructionExample'] = {}
            obj['instructionExample']['link'] = obj['instruction_link']
            obj['instructionExample']['value'] = 'view'

            new_obj = copy_object(obj, headers)
            new_data.append(new_obj)

    elif (tablename == 'matching_column'):
        data = list(Model.objects.all().values('id','report__name', 'journey_column', 'report_column', 'function'))
        headers = ['id','report', 'journey_column', 'report_column', 'function']
        new_data = data
    else:
        data = list(Model.objects.all().values())
        new_data = data
        headers = []
        for field in Model._meta.fields:
            if type(field) != "<class 'django.db.models.fields.reverse_related.ManyToOneRel'>":
                headers.append(field.name)

    return render(request, "journey/base-table.html", {'data': new_data, 'tableName': tablename, 'headers': headers})


@login_required(login_url="/authentication/login")
def create_form_data(request, tablename):
    Model = apps.get_model(app_label="journey", model_name=tablename)
    FormModel = formData[tablename]

    form = FormModel()
    if request.method == "POST":
        form = FormModel(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/journey/table/" + tablename)

    return render(request, "journey/base-form.html", {'formName': 'Form ' + tablename, 'form': form})


@login_required(login_url="/authentication/login")
def update_form_data(request, tablename, id=None):
    Model = apps.get_model(app_label="journey", model_name=tablename)
    FormModel = formData[tablename]

    obj = get_object_or_404(Model, pk=id)
    form = FormModel(instance=obj)
    if request.method == "POST":
        form = FormModel(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("/journey/table/" + tablename)
        print(form.errors)
    
    return render(request, "journey/base-form.html", {'formName': 'Form ' + tablename, 'form': form})


@login_required(login_url="/authentication/login")
def delete_form_data(request, tablename, id=None):
    Model = apps.get_model(app_label="journey", model_name=tablename)
    FormModel = formData[tablename]

    obj = get_object_or_404(Model, pk=id)
    obj.delete()
    return redirect("/journey/table/" + tablename)


@login_required(login_url="/authentication/login")
def import_touchpoint(request):
    all_fields = {}
    matching_reports = [report for report in Matching_Report.objects.all()]
    matched_columns = [{'report_name': column.report.name,
                        'report_column': column.report_column,
                        'journey_column': column.journey_column,
                        'function': column.function
                        } for column in Matching_Column.objects.all()]

    for field in Touchpoint._meta.get_fields():
        if (field.name != "id" and field.name != "record_time"):
            data_type = field.get_internal_type()
            converted_type = ""

            if (data_type == "BigIntegerField" or data_type == "IntegerField" or data_type == "FloatField"):
                converted_type = "numeric"
            elif (data_type == "DateTimeField" or data_type == "DataField"):
                converted_type = "date"
            else:
                converted_type = "string"

            all_fields[field.name] = converted_type

    return render(request, "journey/import-touchpoint.html", {"allFields": all_fields, "matchingReports": matching_reports, "matchedColumns": matched_columns})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def track_geo_info(request, data):
    ip = get_client_ip(request)
    g = GeoIP2()

    try:
        geolocation = g.city(ip)
        data['geo_continent'] = geolocation['time_zone']
        data['geo_country'] = geolocation['country_name']
        data['geo_city'] = geolocation['city']
    except:
        pass

    return data

def track_device_info(request, data):
    data['device_browser'] = request.user_agent.browser.family
    data['device_os'] = request.user_agent.os.family

    if (request.user_agent.is_mobile):
        data['device_category'] = 'mobile'
    elif (request.user_agent.is_mobile):
        data['device_category'] = 'tablet'
    elif (request.user_agent.is_pc):
        data['device_category'] = 'desktop'

    return data

@csrf_exempt
def add_new_touchpoint(req):
    body = json.loads(req.body)
    data = body["data"]
    data = track_device_info(req, data)
    data = track_geo_info(req, data)

    print(data)

    new_touchpoint = create_new_touchpoint(data)
    new_touchpoint.save()

    return HttpResponse()

@login_required(login_url="/authentication/login")
def read_instruction(request):
    matching_reports = [report for report in Matching_Report.objects.all()]

    return render(request, "journey/read-instruction.html", {"matchingReports": matching_reports})


@login_required(login_url="/authentication/login")
def export_touchpoint(request):
    return render(request, "journey/export-touchpoint.html")

@login_required(login_url="/authentication/login")
@csrf_exempt
def upload_touchpoint(request):
    if request.method == "POST":
        body = json.loads(request.body)
        touchpoints = body["data"]
        new_touchpoints = []

        for touchpoint in touchpoints:
            new_touchpoint = create_new_touchpoint(touchpoint)
            new_touchpoints.append(new_touchpoint)

        for new_touchpoint in new_touchpoints:
            new_touchpoint.save()

        return JsonResponse({"result": "Import Successfully"})


def create_new_touchpoint(touchpoint):
    new_touchpoint = Touchpoint()
    for key in touchpoint:
        value = touchpoint[key]
        if (value == '' or value is None):
            continue
        if key == "action_type":
            new_value = get_or_none(Action_Type, value, key)
        elif key == "traffic_source_name":
            new_value = get_or_none(Traffic_Source_Type, value, key)
        elif key == "channel_type":
            new_value = get_or_none(Channel_Type, value, key)
        elif key == "device_browser":
            new_value = get_or_none(Device_Browser, value, key)
        elif key == "device_os":
            new_value = get_or_none(Device_OS, value, key)
        elif key == "device_category":
            new_value = get_or_none(Device_Category, value, key)
        elif key == "interact_item_type":
            new_value = get_or_none(Interact_Item_Type, value, key)
        elif key == "experience_emotion":
            new_value = get_or_none(Experience_Emotion, value, key)
        else:
            new_value = value

        if isinstance(new_value, dict) and "error" in new_value:
            print(new_value["error"])
            return JsonResponse({"result": new_value["error"]})
        else:
            setattr(new_touchpoint, key, new_value)
    
    return new_touchpoint


def get_or_none(classmodel, name, column):
    try:
        return classmodel.objects.get(name=name)
    except classmodel.MultipleObjectsReturned:
        return {"error": "At column " + column + ", " + name + " is not an appropriate value"}
    except classmodel.DoesNotExist:
        obj = classmodel.objects.create(name=name)
        obj.save()
        return obj


def read_detail_instruction(request, datasrc):
    listMatchingFields = [[row.report_column, row.journey_column, row.function]
                          for row in Matching_Column.objects.filter(report__name=datasrc)]
    instruction_img = Matching_Report.objects.get(
        name=datasrc).instruction_link
    return render(request, "journey/read-detail-instruction.html", {'dataSrc': datasrc.upper(), 'listMatchingFields': listMatchingFields, 'instructionImg': instruction_img})


@login_required(login_url="/authentication/login")
def create_mapping_file(request):
    journey_columns = [column.name for column in Touchpoint._meta.get_fields(
    ) if column.name != 'id' and column.name != 'report_time']
    reports = [report.name for report in Matching_Report.objects.all()]
    functions = ['lower', 'upper', 'datetime', 'string', 'int', 'float']
    return render(request, "journey/create-mapping-file.html", {'reports': reports, 'journeyColumns': journey_columns, 'functions': functions})


@login_required(login_url="/authentication/login")
@csrf_exempt
def upload_mapping_file(request):
    if request.method == "POST":
        data_source = request.POST.get('dataSrc')
        matching_columns = json.loads(request.POST.get('matchingColumns'))
        files = request.FILES.getlist('files[]')

        link_url = ''

        if (len(files) > 0):
            instructionImg = files[0]

            filename = 'journey/instructions/' + str(datetime.now().timestamp()) + ".png"

            (static_path, link_url) = get_static_path(filename, 'journey')

            handle_uploaded_file(instructionImg, static_path)

        new_report = Matching_Report.objects.create(
            name=data_source, instruction_link=link_url)
        new_report.save()

        for column in matching_columns:
            new_matching_column = Matching_Column.objects.create(report=new_report,
                                                                 journey_column=column['journey_column'],
                                                                 report_column=column['report_column'],
                                                                 function=column['function'])
            new_matching_column.save()

        return JsonResponse({"result": "Create Successfully"})


def handle_uploaded_file(f, path):
    destination = open(path, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
