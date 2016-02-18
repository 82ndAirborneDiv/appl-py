from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectOverview,IosProject,IosRelease,AndroidProject,AndroidRelease

@login_required()
def home_page(request):

    apps_to_display = ProjectOverview.objects.filter(project__in=Project.objects.filter(is_archived=False).order_by('title'))
    for app in apps_to_display:
        androidRelease =    AndroidRelease.objects.select_related('android_project__project_overview').filter(android_project__project_overview__project_id=app.project_id).order_by('-timestamp')
        iosRelease =        IosRelease.objects.select_related('ios_project__project_overview').filter(ios_project__project_overview__project_id=app.project_id).order_by('-timestamp')
        app.android =  androidRelease[0]
        app.ios = iosRelease[0]

    return render(request, 'applab/home.html', {'apps': apps_to_display})

def login(request):
    return render(request, 'applab/templates/registration/login.html')
