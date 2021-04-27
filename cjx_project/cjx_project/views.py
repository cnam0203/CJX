
from django.shortcuts import redirect

def redirectHomepage(req):
    return redirect('/admin/')