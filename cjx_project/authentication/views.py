from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt
def login_page(request):
    if request.user.is_authenticated:
        return redirect("/journey/home")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/journey/home')
        else:
            return render(request, "authentication/login.html")

    return render(request, "authentication/login.html")

def logout_page(request):
    logout(request)
    return redirect("/authentication/login")