from django.shortcuts import render


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
