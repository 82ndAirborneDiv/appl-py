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
    historyLimit = 6
    platform = project_title.split('-')[0]
    appTitle = ' '.join(project_title.split('-')[1:-4])
    appRelease = project_title.rsplit('-')[-4:]

    appOverview = ProjectOverview.objects.filter(project__in=Project.objects.filter(is_archived=False, title = appTitle))[0]
    screenshots = ProjectOverviewScreenshot.objects.filter(project_overview = appOverview.project_id)

    if platform == 'ios':
        curRelease = IosRelease.objects.select_related('ios_project__project_overview').filter(ios_project__project_overview__project_id=appOverview.project_id,major_version=appRelease[0],minor_version=appRelease[1],point_version=appRelease[2],build_version=appRelease[3])[0]
        previousReleases = IosRelease.objects.select_related('ios_project__project_overview').filter(ios_project__project_overview__project_id=appOverview.project_id).order_by('-major_version','-minor_version','-point_version','-build_version')[1:historyLimit+1]
    elif platform == 'android':
        curRelease = AndroidRelease.objects.select_related('android_project__project_overview').filter(android_project__project_overview__project_id=appOverview.project_id,major_version=appRelease[0],minor_version=appRelease[1],point_version=appRelease[2],build_version=appRelease[3])[0]
        previousReleases = AndroidRelease.objects.select_related('ios_project__project_overview').filter(android_project__project_overview__project_id=appOverview.project_id).order_by('-major_version','-minor_version','-point_version','-build_version')[1:historyLimit+1   ]
    appDetail = {
        'overview' : appOverview,
        'releaseDetail': curRelease,
        'previousRelease' : previousReleases,
        'screenshotGroups': [screenshots[i:i + groupSize] for i in range(0, len(screenshots), groupSize)],
        'title': appTitle,
        'platform': platform,
        'releaseVersion': '.'.join(appRelease)
    }
    #appDetail.appRelease = '{0}.{1}.{2}.{3}'.format(appDetail.major_version,appDetail.minor_version,appDetail.point_version,appDetail.build_version)
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

def platform_page(request,platform,sortfield=None):
    platform_app = {}
    if sortfield:
        sortfield = sortfield.lower()
        if sortfield =='sortname':
           sortfield = platform + '_project__project_overview__project__title'
        if sortfield =='sortnamedesc':
           sortfield = '-'+ platform + '_project__project_overview__project__title'
        elif sortfield == 'sortreleasedate':
            sortfield = '-timestamp'
    else:
        sortfield = '-timestamp'

    if platform == 'ios':
       apps = IosRelease.objects.select_related('ios_project__project_overview__project').exclude(ios_project__project_overview__project__is_archived = True).order_by(sortfield)
       for app in apps:
           app.title = app.ios_project.project_overview.project.title
           app.icon_url =  app.ios_project.project_overview.icon.url
           app.description = app.ios_project.project_overview.description
    elif platform == 'android':
       apps = AndroidRelease.objects.select_related('android_project__project_overview__project').exclude(android_project__project_overview__project__is_archived = True).order_by(sortfield)
       for app in apps:
           app.title = app.android_project.project_overview.project.title
           app.icon_url =  app.android_project.project_overview.icon.url
           app.description = app.android_project.project_overview.description
    platform_app['apps'] = apps
    platform_app['platform'] = platform

    return render(request,'applab/platform-page.html/', {
        'platform_app' : platform_app
    })

#days = forms.ModelChoiceField(queryset=Day.objects.all().order_by('alias'), widget=forms.Select(attrs={"onChange":'refresh()'}))