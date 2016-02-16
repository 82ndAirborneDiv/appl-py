from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectOverview

@login_required()
def home_page(request):
    projects_to_display = ProjectOverview.objects.filter(project__in=Project.objects.filter(is_archived=False).order_by('title'))
    projects_ordered = projects_to_display.order_by()

    return render(request, 'applab/home.html', {'projects': projects_to_display})


def login(request):
    return render(request, 'applab/templates/registration/login.html')



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
