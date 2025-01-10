from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            print('Password matches!')
        else:
            messages.info(request, 'Password does not match!')
    else:
        return render(request, 'signup.html')

def logout(request):
    pass