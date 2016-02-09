from django.shortcuts import render
from django.http import Http404
from apps.models import App

def hello_world(request):
    return render(request, 'applab/hello_world.html')


def login(request):
    return render(request, 'applab/login.html')


def home(request):
    return render(request, 'applab/home.html')


def ios(request):
    return render(request, 'applab/ios.html')


def android(request):
    return render(request, 'applab/android.html')

def app_detail(request,app_id):
    try:
        app =  App.objects.get(app_id = app_id)
    except App.DoesNotExist:
        raise Http404('This app does not exist')
    return render(request,'applab/app_detail.html',{
        'app' : app,
    })
