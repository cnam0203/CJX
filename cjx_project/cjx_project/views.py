
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json

def redirectHomepage(req):
    return redirect('/journey/home')

