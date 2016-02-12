from django.shortcuts import render
from django.http import Http404
from .models import Project

def hello_world(request):
    return render(request, 'applab/hello_world.html')


def login(request):
    return render(request, 'applab/login.html')


def home(request):
    try:
        newReleases = Project.objects.filter(is_archived = 0)
    except Project.DoesNotExist:
        newReleases = []
    return render(request, 'applab/home.html', {
        'newReleases' : newReleases,
    })


def ios(request):
    return render(request, 'applab/ios.html')


def android(request):
    return render(request, 'applab/android.html')

def app_detail(request):
    try:
        app =  Project.objects.get(is_archived=False)
    except Project.DoesNotExist:
        raise Http404('This app does not exist')
    return render(request,'applab/app_detail.html',{
        'app' : app,
    })
