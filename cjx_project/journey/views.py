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
from django.db.models import F
from django.db.models.functions import TruncDate


from .models import Touchpoint, Journey_Customer, Action_Type, Channel_Type, Traffic_Source_Type, Device_Browser, Device_OS, Device_Category, Device_Category, Interact_Item_Type, Experience_Emotion, Matching_Report, Matching_Column
from .constant import formData, functions, documentation_pages

from utils.path_helper import get_static_path
from utils.copy_object import copy_object
from datetime import datetime
from datetime import date
from json import dumps
from authentication.models import API_KEY

import json
import os

# Create your views here.
@login_required(login_url="/authentication/login")
def create_mapping_file(request):
    journey_columns     = [column.name for column in Touchpoint._meta.get_fields() 
                                if column.name != 'id' and column.name != 'report_time']
    reports             = [report.name for report in Matching_Report.objects.all()]

    return render(
                    request, 
                    "journey/create-mapping-file.html", 
                    {
                        'reports'       : reports, 
                        'journeyColumns': journey_columns, 
                        'functions'     : functions
                    }
                )


@login_required(login_url="/authentication/login")
def upload_mapping_file(request):
    if request.method == "POST":
        mapping_file_name   = request.POST.get('mappingFileName')
        mapping_columns     = json.loads(request.POST.get('mappingColumns'))
        files               = request.FILES.getlist('files[]')
        link_url            = ''

        # If mapping file contains instruction image, save image in static file
        if (len(files)):
            instructionImg          = files[0]
            filename                = 'journey/instructions/' + str(datetime.now().timestamp()) + ".png"
            (static_path, link_url) = get_static_path(filename, 'journey')
            handle_uploaded_file(instructionImg, static_path)

        # Insert into Matching_Report table new row for information of mapping file
        new_report = Matching_Report.objects.create(name=mapping_file_name, instruction_link=link_url)
        new_report.save()

        # For each mapping columns in mapping file, insert it into Matching_Column table
        for column in mapping_columns:
            new_matching_column = Matching_Column.objects.create(report=new_report,
                                                                 journey_column=column['journey_column'],
                                                                 report_column=column['report_column'],
                                                                 function=column['function'])
            new_matching_column.save()

        return JsonResponse({"status": 200, "result": "Create Successfully"})

    return JsonResponse({"status": 400, "result": "Upload failed"})


@login_required(login_url="/authentication/login")
def import_touchpoint(request):
    all_fields          =   {}
    matching_reports    =   [report for report in Matching_Report.objects.all()]
    matched_columns     =   [
                                {'report_name': column.report.name,
                                    'report_column': column.report_column,
                                    'journey_column': column.journey_column,
                                    'function': column.function
                                } for column in Matching_Column.objects.all()
                            ]

    for field in Touchpoint._meta.get_fields():
        if (field.name != "id" and field.name != "record_time"):
            data_type       = field.get_internal_type()
            converted_type  = ""

            if (data_type == "BigIntegerField" or data_type == "IntegerField" or data_type == "FloatField"):
                converted_type = "numeric"
            elif (data_type == "DateTimeField" or data_type == "DataField"):
                converted_type = "date"
            else:
                converted_type = "string"

            all_fields[field.name] = converted_type

    return render(
                    request, 
                    "journey/import-touchpoint.html", 
                    {
                        "allFields"         : all_fields, 
                        "matchingReports"   : matching_reports, 
                        "matchedColumns"    : matched_columns
                    }
                )


@login_required(login_url="/authentication/login")
def import_csv_file(request):
    if request.method == "POST":
        body = json.loads(request.body)
        import_touchpoints = body["data"]
        valid_touchpoints = []

        for touchpoint in import_touchpoints:
            # Check field in touchpoint valid
            valid_touchpoint = create_valid_touchpoint(touchpoint)

            if (valid_touchpoint):      # If valid, add valid touchpoint in list valid touchpoints
                valid_touchpoints.append(valid_touchpoint)
            else:                       # If invalid, response import failed
                return JsonResponse({"status": 400, "result": "Import failed"})

        for valid_touchpoint in valid_touchpoints:
            valid_touchpoint.save()   # Add valid touchpoint in database

        return JsonResponse({"status": 200, "result": "Import Successfully"})

    return JsonResponse({"status": 400, "result": "Import failed"})



@login_required(login_url="/authentication/login")
def read_detail_instruction(request, datasrc):
    listMatchingFields  = [[row.report_column, row.journey_column, row.function]
                                for row in Matching_Column.objects.filter(report__name=datasrc)]
    instruction_img     = Matching_Report.objects.get(name=datasrc).instruction_link
    return render(
                    request, 
                    "journey/read-detail-instruction.html", 
                    {
                        'dataSrc'           : datasrc.upper(), 
                        'listMatchingFields': listMatchingFields, 
                        'instructionImg'    : instruction_img
                    }
                )


@login_required(login_url="/authentication/login")
def read_instruction(request):
    matching_reports = [report for report in Matching_Report.objects.all()]
    return render(
                    request, 
                    "journey/read-instruction.html", 
                    {
                        "matchingReports": matching_reports
                    }
                )


@login_required(login_url="/authentication/login")
def report(request):
    startDate, endDate  = get_period(request)
    list_report = []
    list_attributes = ['action_type', 'channel_type', 'device_category', 'device_os', 'device_browser']

    total_user_chart = get_total_user_chart(startDate, endDate)
    total_touchpoint_chart = get_total_touchpoint_chart(startDate, endDate)

    list_report.append({
                        'title' : 'Total Customer By Day',
                        'data'  : total_user_chart,
                        'type': 1
                    })

    list_report.append({
                        'title' : 'Total Touchpoint By Day',
                        'data'  : total_touchpoint_chart,
                        'type': 1
                    })

    
    for attribute in list_attributes:
        total_touchpoint_by_item = get_total_item_chart(startDate, endDate, attribute)
        list_report.append({
                            'title' : 'Total Touchpoint By ' + attribute.upper() + ' By Day',
                            'data'  : total_touchpoint_by_item,
                            'type': 2
                        })
    
    return render(
                    request, 
                    "journey/report.html",
                    {
                        "reports": dumps(list_report)
                    }
                )


@login_required(login_url="/authentication/login")
def documentation(request):
    return render(
                    request, 
                    "journey/documentation.html", 
                    {
                        'items': documentation_pages
                    }
                )


@login_required(login_url="/authentication/login")
def detail_documentation(request, name):
    documentation_page = {}
    for page in documentation_pages:
        if page['name'] == name:
            documentation_page = page
            break

    return render(
                    request, 
                    documentation_page['html_file'], 
                    {
                        "previous_content"  : documentation_page['previous_content'],
                        "previous_href"     : documentation_page['previous_href'],
                        "next_content"      : documentation_page['next_content'],
                        "next_href"         : documentation_page['next_href']
                    }
                )


@login_required(login_url="/authentication/login")
def home(request):
    total_customer          = len(Journey_Customer.objects.values('customerID').distinct())
    new_customer            = len(Journey_Customer.objects.filter(register_date__year=date.today().year,
                                                            register_date__month=date.today().month,
                                                            register_date__day=date.today().day).values('customerID').distinct())
    activites               = list(Touchpoint.objects.order_by('-time').values('customer_id', 'time', 'action_type__name', 'channel_type__name', 'device_category__name', 'experience_emotion')[:5])
    device_category_data    = get_report_data('device_category', 1)
    channel_type_data       = get_report_data('channel_type', 2)
    event_data              = get_report_data('action_type', 1)
    
    return render(
                    request, 
                    "journey/home.html", 
                    {
                        'activities'            : activites, 
                        'total_customer'        : total_customer, 
                        'new_customer'          : new_customer,
                        'device_category_data'  : device_category_data,
                        'channel_type_data'     : channel_type_data,
                        'event_data'            : event_data
                    }
                )

@login_required(login_url="/authentication/login")
def get_list_data(request, tablename):
    Model       = apps.get_model(app_label="journey", model_name=tablename)
    new_data    = []
    headers     = []

    if (tablename == 'touchpoint'):
        new_data    = list(Model.objects.all().order_by('-id').values('id', 'customer_id', 'action_type__name', 'time', 'channel_type__name',
                    'device_browser__name', 'device_os__name', 'device_category__name', 'geo_continent',
                    'geo_country', 'geo_city', 'interact_item_type__name', 'interact_item_content',
                    'experience_emotion__name'))
        headers     = ['id', 'customer_id', 'action_type', 'time', 'channel_type',
                        'browser', 'os', 'device_category', 'geo_continent',
                        'geo_country', 'geo_city', 'interact_item_type', 'interact_item_content',
                        'experience']

    elif (tablename == 'matching_report'):
        data        = list(Model.objects.all().values())
        headers     = ['id', 'name', 'instructionExample']

        for obj in data:
            obj['instructionExample']           = {}
            obj['instructionExample']['link']   = obj['instruction_link']
            obj['instructionExample']['value']  = 'view'

            new_obj = copy_object(obj, headers)
            new_data.append(new_obj)

    elif (tablename == 'matching_column'):
        new_data    = list(Model.objects.all().values('id','report__name', 'journey_column', 'report_column', 'function'))
        headers     = ['id','report', 'journey_column', 'report_column', 'function']

    else:
        new_data    = list(Model.objects.all().values())
        headers     = []
        for field in Model._meta.fields:
            if type(field) != "<class 'django.db.models.fields.reverse_related.ManyToOneRel'>":
                headers.append(field.name)

    return render(
                    request, 
                    "journey/base-table.html", 
                    {
                        'data'      : new_data, 
                        'tableName' : tablename, 
                        'headers'   : headers
                    }
                )




@login_required(login_url="/authentication/login")
def create_form_data(request, tablename):
    Model       = apps.get_model(app_label="journey", model_name=tablename)
    FormModel   = formData[tablename]
    form        = FormModel()

    if request.method == "POST":
        form = FormModel(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/journey/table/" + tablename)

    return render(
                    request, 
                    "journey/base-form.html", 
                    {
                        'formName'  : 'Form ' + tablename, 
                        'form'      : form
                    }
                )


@login_required(login_url="/authentication/login")
def update_form_data(request, tablename, id=None):
    Model       = apps.get_model(app_label="journey", model_name=tablename)
    FormModel   = formData[tablename]

    obj         = get_object_or_404(Model, pk=id)
    form        = FormModel(instance=obj)

    if request.method == "POST":
        form = FormModel(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("/journey/table/" + tablename)
    
    return render(
                    request, 
                    "journey/base-form.html", 
                    {
                        'formName'  : 'Form ' + tablename, 
                        'form'      : form
                    }
                )


@login_required(login_url="/authentication/login")
def delete_form_data(request, tablename, id=None):
    Model       = apps.get_model(app_label="journey", model_name=tablename)
    FormModel   = formData[tablename]

    obj         = get_object_or_404(Model, pk=id)
    obj.delete()

    return redirect("/journey/table/" + tablename)


@login_required(login_url="/authentication/login")
def get_import_page(request):
    all_fields          =   {}
    matching_reports    =   [report for report in Matching_Report.objects.all()]
    matched_columns     =   [
                                {
                                    'report_name'   : column.report.name,
                                    'report_column' : column.report_column,
                                    'journey_column': column.journey_column,
                                    'function'      : column.function
                                } for column in Matching_Column.objects.all()
                            ]

    for field in Touchpoint._meta.get_fields():
        if (field.name != "id" and field.name != "record_time"):
            data_type       = field.get_internal_type()
            converted_type  = ""

            if (data_type == "BigIntegerField" or data_type == "IntegerField" or data_type == "FloatField"):
                converted_type = "numeric"
            elif (data_type == "DateTimeField" or data_type == "DataField"):
                converted_type = "date"
            else:
                converted_type = "string"

            all_fields[field.name] = converted_type

    return render(
                    request, 
                    "journey/import.html", 
                    {
                        "allFields"         : all_fields, 
                        "matchingReports"   : matching_reports, 
                        "matchedColumns"    : matched_columns
                    }
                )


@login_required(login_url="/authentication/login")
def get_create_mapping_file(request):
    fields  = [field.name for field in Touchpoint._meta.get_fields() 
                            if field.name != 'id' and field.name != 'report_time']
    reports = [report.name for report in Matching_Report.objects.all()]
    return render(
                    request, 
                    "journey/mapping-file.html", 
                    {
                        'reports'   : reports,
                        'fields'    : fields,
                        'functions' : functions
                    }
                )


@login_required(login_url="/authentication/login")
def review_mapping_file(request, dataSrcName=None):
    matching_reports        = [report for report in Matching_Report.objects.all()]
    list_matching_fields    = []
    instruction_img         = None

    if (dataSrcName is not None):
        list_matching_fields    = [[row.report_column, row.journey_column, row.function]
                                    for row in Matching_Column.objects.filter(report__name=dataSrcName)]
        instruction_img         = Matching_Report.objects.get(name=dataSrcName).instruction_link

    return render(
                    request, 
                    "journey/review-mapping.html", 
                    {
                        "dataSrcs"          : matching_reports, 
                        "dataSrcName"       : dataSrcName, 
                        "listMatchingFields": list_matching_fields,
                        "instructionImg"    : instruction_img
                    }
                )


@csrf_exempt
def import_touchpoint_api(req):
    if (req.method == 'POST'):
        headers = req.headers
        message = ''
        # Check api_access_token
        if ('Authorization' in headers):
            api_token = headers['Authorization'].split(' ')[1]
            tokens = list(API_KEY.objects.filter(key=api_token))
            # If access_token is valid
            if (len(tokens) > 0):
                if (req.body):
                    # Load data in request body
                    data = json.loads(req.body)['data']
                    # Find device info based on http request
                    data = track_device_info(req, data)
                    # Find geo network based on http request
                    data = track_geo_info(req, data)

                    # Check touchpoint is valid
                    new_touchpoint = create_valid_touchpoint(data)
                    if (new_touchpoint):
                        new_touchpoint.save()
                        return JsonResponse({'status': 200, 'message': 'Add new touchpoint successfully'})
                    else:
                        message = 'Import touchpoint may be wrong format'
                else:
                    message = 'Require data in body'
            else:
                message = 'Authentication failed'
        else:
            message = 'Require API Token'
    else:
        message = 'HTTP method is wrong'
    
    return JsonResponse({'status': 400, 'message': message})

def get_total_user_chart(startDate, endDate):
    total_customer_by_day = list(Touchpoint.objects.filter(time__range=[startDate, endDate]).annotate(date=TruncDate('time')).values('date').annotate(total=Count('customer_id', distinct=True)).order_by('date'))
    report_data = []

    if (len(total_customer_by_day) != 0):
        report_data = [[item['date'].strftime("%d-%m-%Y"), item['total']] for item in total_customer_by_day]

    return report_data

def get_total_touchpoint_chart(startDate, endDate):
    total_touchpoint_by_day = list(Touchpoint.objects.filter(time__range=[startDate, endDate]).annotate(date=TruncDate('time')).values('date').annotate(total=Count('id')).order_by('date'))
    report_data = []

    if (len(total_touchpoint_by_day) != 0):
        report_data = [[item['date'].strftime("%d-%m-%Y"), item['total']] for item in total_touchpoint_by_day]
    return report_data

def get_total_item_chart(startDate, endDate, report):
    column_name = report + '__name'
    total_item_by_date = list(Touchpoint.objects.filter(time__range=[startDate, endDate]).annotate(date=TruncDate('time')).values('date', column_name).annotate(total=Count('id')).order_by('date', column_name))
    report_data = []

    if (len(total_item_by_date) != 0):
        report_data = [[item['date'].strftime("%d-%m-%Y"), item['total'], item[column_name]] for item in total_item_by_date]
    return report_data

def get_report_data(report, type):
    column_name     =   report + '__name'
    total_usage     =   len(Touchpoint.objects.all())
    report_usage    =   list(Touchpoint.objects.all().values(column_name).annotate(total=Count(column_name)))
    report_data     =   []

    if (len(report_usage) != 0 and (report_usage[0][column_name] != 'None' or report_usage[0]['total'] != 0)):
        if (type == 1):
            report_data     =   [[item[column_name],(item['total']/total_usage)*100] for item in report_usage]
        else:
            report_data     =   [{'name': item[column_name], 'y': (item['total']/total_usage)*100} for item in report_usage]

    return dumps(report_data)
    

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def track_geo_info(request, data):
    ip  = get_client_ip(request)
    g   = GeoIP2()
    try:
        geolocation             = g.city(ip)
        data['geo_continent']   = geolocation['time_zone']
        data['geo_country']     = geolocation['country_name']
        data['geo_city']        = geolocation['city']
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


def create_valid_touchpoint(touchpoint):
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
            return False
        else:
            setattr(new_touchpoint, key, new_value)
    
    return new_touchpoint


def get_period(request):
    startDate = datetime(2000, 1, 1)
    endDate = datetime.now()
    if (request.method == "POST"):
        if (request.POST["startDate"] != ''):
            startDate = request.POST["startDate"]
        if (request.POST["endDate"] != ''):
            endDate = request.POST["endDate"]

    return startDate, endDate

def get_or_none(classmodel, name, column):
    try:
        return classmodel.objects.get(name=name)
    except classmodel.MultipleObjectsReturned:
        return {"error": "At column " + column + ", " + name + " is not an appropriate value"}
    except classmodel.DoesNotExist:
        obj = classmodel.objects.create(name=name)
        obj.save()
        return obj


def handle_uploaded_file(f, path):
    destination = open(path, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()





    
    
