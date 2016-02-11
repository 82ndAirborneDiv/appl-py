from django.shortcuts import render

def hello_world(request):
    return render(request, 'applab/hello_world.html')

def login(request):
    return render(request, 'applab/login.html')
