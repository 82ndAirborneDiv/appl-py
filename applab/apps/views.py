from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectOverview,IosProject,IosRelease,AndroidProject,AndroidRelease, ProjectOverviewScreenshot

@login_required()
def home_page(request):

    apps_to_display = ProjectOverview.objects.filter(project__in=Project.objects.filter(is_archived=False).order_by('title'))
    for app in apps_to_display:
        androidRelease =    AndroidRelease.objects.select_related('android_project__project_overview').filter(android_project__project_overview__project_id=app.project_id).order_by('-major_version','-minor_version','-point_version','-build_version')
        iosRelease =        IosRelease.objects.select_related('ios_project__project_overview').filter(ios_project__project_overview__project_id=app.project_id).order_by('-major_version','-minor_version','-point_version','-build_version')
        try:
            app.android =  androidRelease[0]
        except IndexError:
            app.android = None
        try:
            app.ios = iosRelease[0]
        except IndexError:
            app.ios = None;
        app.screenshots =  ProjectOverviewScreenshot.objects.filter(project_overview = app.project_id)

    return render(request, 'applab/home.html', {'apps': apps_to_display})

def login(request):
    return render(request, 'applab/templates/registration/login.html')

def ios_page(request):
    #apps = IosProject.objects.select_related('project_overview').exclude(project_overview__project__is_archived = True).order_by('project_overview__project__title')
    apps = IosRelease.objects.select_related('ios_project').exclude(ios_project__project_overview__project__is_archived = True).order_by('-timestamp')
    return render(request,'applab/ios.html', {
        'apps' : apps,
    })

def android_page(request):
    #apps = AndroidProject.objects.select_related('project_overview').exclude(project_overview__project__is_archived = True)
    apps = AndroidRelease.objects.select_related('android_project').exclude(android_project__project_overview__project__is_archived = True).order_by('-timestamp')
    return render(request,'applab/android.html', {
        'apps' : apps,
    })


def app_page(request,project_title):
    groupSize = 4
    platform = project_title.split('-')[0]
    app_title = ' '.join(project_title.split('-')[1:])
    appDetail = ProjectOverview.objects.filter(project__in=Project.objects.filter(is_archived=False, title = app_title).order_by('title'))
    screenshots = ProjectOverviewScreenshot.objects.filter(project_overview = appDetail)
    screenshotGroups = [screenshots[i:i+groupSize] for i in range(0, len(screenshots), groupSize)]
    # appDetail.screenshotGroups = screenshotGroups
    # appDetail.title = app_title
    # appDetail.platform = platform
    # app_version = []
    # appRelease = {
    #     'major' : app_version[0],
    #     'minor' : app_version[1],
    #     'point' : app_version[2],
    #     'version': app_version[3],
    #
    # }
    return render(request,'applab/app-page.html/',{
        'appDetail' : appDetail,
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