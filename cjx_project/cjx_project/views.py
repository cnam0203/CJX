
from django.shortcuts import redirect

import json

def redirectHomepage(req):
    return redirect('/journey/home')

