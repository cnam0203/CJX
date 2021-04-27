from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import JsonResponse

from django.db import Error
from django.db import DataError
from django.db import DatabaseError
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from datetime import datetime

from .models import Touchpoint
from .models import Action_Type
from .models import Channel_Type
from .models import Source_Type
from .models import Device_Browser
from .models import Device_OS
from .models import Device_OS
from .models import Device_Category
from .models import Interact_Item_Type
from .models import Experience_Emotion
from .models import Matching_Report
from .models import Matching_Column

import json
import os

from utils.path_helper import get_static_path
# Create your views here.



@user_passes_test(lambda user: user.is_staff, login_url="/admin")
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


@user_passes_test(lambda user: user.is_staff, login_url="/admin")
def read_instruction(request):
    matching_reports = [report for report in Matching_Report.objects.all()]

    return render(request, "journey/read-instruction.html", {"matchingReports": matching_reports})


@user_passes_test(lambda user: user.is_staff, login_url="/admin")
def export_touchpoint(request):
    return render(request, "journey/export-touchpoint.html")


@user_passes_test(lambda user: user.is_staff, login_url="/admin")
def upload_touchpoint(request):
    if request.method == "POST":
        body = json.loads(request.body)
        touchpoints = body["data"]
        new_touchpoints = []

        for touchpoint in touchpoints:
            new_touchpoint = Touchpoint()
            for key in touchpoint:
                value = touchpoint[key]
                if key == "action_type":
                    new_value = get_or_none(Action_Type, value, key)
                elif key == "source_name":
                    new_value = get_or_none(Source_Type, value, key)
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
                    return JsonResponse({"result": new_value["error"]})
                else:
                    setattr(new_touchpoint, key, new_value)
                    new_touchpoints.append(new_touchpoint)

        for new_touchpoint in new_touchpoints:
            new_touchpoint.save()

        return JsonResponse({"result": "Import Successfully"})


def get_or_none(classmodel, name, column):
    try:
        return classmodel.objects.get(name=name)
    except classmodel.MultipleObjectsReturned:
        return {"error": "At column " + column + ", " + name + " is not an appropriate value"}
    except classmodel.DoesNotExist:
        if name is None:
            obj = classmodel.objects.create(name=name)
            obj.save()
            return obj
        else:
            return {"error": "At column " + column + ", " + name + " is not an appropriate value"}


@user_passes_test(lambda user: user.is_staff, login_url="/admin")
def read_detail_instruction(request, datasrc):
    listMatchingFields = [[row.report_column, row.journey_column, row.function]
                          for row in Matching_Column.objects.filter(report__name=datasrc)]
    instruction_img = Matching_Report.objects.get(
        name=datasrc).instruction_link
    return render(request, "journey/read-detail-instruction.html", {'dataSrc': datasrc.upper(), 'listMatchingFields': listMatchingFields, 'instructionImg': instruction_img})


@user_passes_test(lambda user: user.is_staff, login_url="/admin")
def create_mapping_file(request):
    journey_columns = [column.name for column in Touchpoint._meta.get_fields(
    ) if column.name != 'id' and column.name != 'report_time']
    reports = [report.name for report in Matching_Report.objects.all()]
    functions = ['lower', 'upper', 'datetime', 'string', 'int', 'float']
    return render(request, "journey/create-mapping-file.html", {'reports': reports, 'journeyColumns': journey_columns, 'functions': functions})


@user_passes_test(lambda user: user.is_staff, login_url="/admin")
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
