from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectOverview,IosProject,IosRelease,AndroidProject,AndroidRelease, ProjectOverviewScreenshot

@login_required()
def home_page(request):

    apps_to_display = ProjectOverview.objects.filter(project__in=Project.objects.filter(is_archived=False).order_by('title'))
    for app in apps_to_display:
        androidRelease =    AndroidRelease.objects.select_related('android_project__project_overview').filter(android_project__project_overview__project_id=app.project_id).order_by('-major_version','-minor_version','-point_version','-build_version')
        iosRelease =        IosRelease.objects.select_related('ios_project__project_overview').filter(ios_project__project_overview__project_id=app.project_id).order_by('-major_version','-minor_version','-point_version','-build_version')
        app.android =  androidRelease[0]
        app.ios = iosRelease[0]
        app.screenshots =  ProjectOverviewScreenshot.objects.filter(project_overview = app.project_id)

    return render(request, 'applab/home.html', {'apps': apps_to_display})

def login(request):
    return render(request, 'applab/templates/registration/login.html')

def app_page(request,release):
    rel_version = release.rsplit('-')
    appDetail = {
        'major' : rel_version[0],
        'minor' : rel_version[1],
        'point' : rel_version[2],
        'version': rel_version[3],

    }
    return render(request,'applab/app-page.html/',{
        'app' : appDetail,
    })

def project_page(request,codename):
    groupSize = 4
    app  = ProjectOverview.objects.filter(project__in=Project.objects.filter(project_code_name = codename))
    screenshots = ProjectOverviewScreenshot.objects.filter(project_overview = '1')
    screenshotGroups = [screenshots[i:i+groupSize] for i in range(0, len(screenshots), groupSize)]
    projectDetail = {
        'hello' : 'Hello',
         'screenshotGroups' : screenshotGroups
    }
    return render(request,'applab/project-page.html/',{
        'projectDetail' : projectDetail,
    })