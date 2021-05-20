
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_ip_geolocation.decorators import with_ip_geolocation

import json

def redirectHomepage(req):
    return redirect('/journey/home')

