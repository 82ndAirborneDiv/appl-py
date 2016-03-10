import copy
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectOverview,IosProject,IosRelease,AndroidProject,AndroidRelease, ProjectOverviewScreenshot
from wsgiref.util import FileWrapper
from django_user_agents.utils import get_user_agent
from .create_manifest import write_manifest

@login_required()
def home_page(request):
    request.session['platform'] = ''
    apps_to_display = []
    avail_apps = ProjectOverview.objects.select_related('project').filter(project__in=Project.objects.filter(is_archived=False))
    for app in avail_apps:
        one_app = {}
        one_app['title'] = app.project.title
        one_app['description'] = app.description
        one_app['icon'] = app.icon
        try:
            release = AndroidRelease.objects.select_related('android_project__project_overview').filter(android_project__project_overview_id = app.id, is_featured_release=True).order_by('-major_version','-minor_version','-point_version','-build_version')[0]
            one_app['platform'] = 'android'
            one_app['releaseDate'] = release.timestamp
            one_app['releaseVersion'] = '{0}.{1}.{2}.{3}'.format(release.major_version,release.major_version,release.point_version,release.build_version)
            one_app['id'] = release.id
            apps_to_display.append(copy.copy(one_app))
        except IndexError:
            pass
        try:
            release =  IosRelease.objects.select_related('ios_project__project_overview').filter(ios_project__project_overview_id=app.id,is_featured_release=True).order_by('-major_version','-minor_version','-point_version','-build_version')[0]
            one_app['platform'] = 'ios'
            one_app['releaseDate'] = release.timestamp
            one_app['releaseVersion'] = '{0}.{1}.{2}.{3}'.format(release.major_version,release.minor_version,release.point_version,release.build_version)
            one_app['id'] = release.id
            apps_to_display.append(copy.copy(one_app))
        except IndexError:
            pass

    return render(request, 'applab/home.html', {'apps': apps_to_display})

def login(request):
    return render(request, 'applab/templates/registration/login.html')

@login_required()
def app_release(request,platform,release_id):
    user_agent = get_user_agent(request)
    request.session['platform'] = platform.lower()
    # if request.META['HTTP_USER_AGENT'].find('iPhone') != -1:
    #     groupSize = 1
    # elif request.META['HTTP_USER_AGENT'].find('iPad') != 1:
    #     groupSize = 2
    # else:
    groupSize = 4
    historyLimit = 6

    # appTitle = ' '.join(project_title.split('-')[1:-4])
    # appRelease = project_title.rsplit('-')[-4:]

    if platform == 'ios':
        curRelease = IosRelease.objects.select_related('ios_project__project_overview__project').filter(id=release_id)[0]
        overview = curRelease.ios_project.project_overview
        previousReleases = IosRelease.objects.filter(ios_project_id=curRelease.ios_project_id).exclude(id=curRelease.id).order_by('-major_version','-minor_version','-point_version','-build_version')[:historyLimit+1]
        latestRelease = IosRelease.objects.filter(ios_project_id=curRelease.ios_project_id).order_by('-major_version','-minor_version','-point_version','-build_version')[0]
        if user_agent.is_mobile:
            ipa_full_url = request.build_absolute_uri(curRelease.ipa_file.url)
            display_image_url = request.build_absolute_uri(overview.icon.url)
            full_size_image_url = request.build_absolute_uri() #need to know what this will be

            write_manifest(curRelease, ipa_full_url, display_image_url, full_size_image_url)
            manifest_file_url = request.build_absolute_uri(curRelease.manifest_file.url)
        else:
            manifest_file_url = request.build_absolute_uri(curRelease.manifest_file.url)
    elif platform == 'android':
        curRelease = AndroidRelease.objects.select_related('android_project__project_overview__project').filter(id=release_id)[0]
        overview = curRelease.android_project.project_overview
        previousReleases = AndroidRelease.objects.filter(android_project_id=curRelease.android_project_id).exclude(id=curRelease.id).order_by('-major_version','-minor_version','-point_version','-build_version')[:historyLimit+1]
        latestRelease = AndroidRelease.objects.filter(android_project_id=curRelease.android_project_id).order_by('-major_version','-minor_version','-point_version','-build_version')[0]
    screenshots = ProjectOverviewScreenshot.objects.filter(project_overview = overview.project_id)
    appDetail = {
        'overview' : overview,
        'currentRelease' : curRelease,
        'previousReleases' : previousReleases,
        'latestRelease' : latestRelease,
        'screenshotGroups4': [screenshots[i:i + groupSize] for i in range(0, len(screenshots), groupSize)],
        'screenshotGroups3': [screenshots[i:i + 3] for i in range(0, len(screenshots), 3)],
        'screenshotGroups2': [screenshots[i:i + 2] for i in range(0, len(screenshots), 2)],
        'screenshotGroups1':[screenshots[i:i + 1] for i in range(0, len(screenshots), 1)],
        'title': overview.project.title,
        'platform': platform,
        'releaseVersion': '{0}.{1}.{2}.{3}'.format(curRelease.major_version,curRelease.minor_version,curRelease.point_version,curRelease.build_version),
        'latestVersion' : '{0}.{1}.{2}.{3}'.format(latestRelease.major_version,latestRelease.minor_version,latestRelease.point_version,latestRelease.build_version),
        'manifestUrl': 'itms-services://?action=download-manifest&url=' + manifest_file_url,
    }
    #appDetail.appRelease = '{0}.{1}.{2}.{3}'.format(appDetail.major_version,appDetail.minor_version,appDetail.point_version,appDetail.build_version)
    return render(request,'applab/app-release-page.html/',{
        'appDetail' : appDetail,
    })

@login_required()
def platform_page(request,platform,sortfield=None):
    request.session['platform'] = platform.lower()
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
           app.release_id = app.id
           app.releaseVersion = '{0}.{1}.{2}.{3}'.format(app.major_version,app.minor_version,app.point_version,app.build_version)
    elif platform == 'android':
       apps = AndroidRelease.objects.select_related('android_project__project_overview__project').exclude(android_project__project_overview__project__is_archived = True).order_by(sortfield)
       for app in apps:
           app.title = app.android_project.project_overview.project.title
           app.icon_url =  app.android_project.project_overview.icon.url
           app.description = app.android_project.project_overview.description
           app.release_id = app.id
           app.releaseVersion = '{0}.{1}.{2}.{3}'.format(app.major_version,app.minor_version,app.point_version,app.build_version)
    platform_app['apps'] = apps
    platform_app['platform'] = platform

    return render(request,'applab/platform-page.html/', {
        'platform_app' : platform_app
    })

@login_required()
def app_download(request, platform, release_id):
    if str.lower(platform) == "ios":
        app = IosRelease.objects.select_related('ios_project__project_overview__project').filter(id=release_id)[0]
        file_name = app.ios_project.project_overview.project.project_code_name
        ipa_file = app.ipa_file
        response = HttpResponse(FileWrapper(ipa_file), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=%s.ipa' % file_name

        return response

    elif str.lower(platform) == "android":
        app = AndroidRelease.objects.select_related('android_project__project_overview__project').filter(id=release_id)[0]

        apk= app.apk_file
        file_name = app.android_project.project_overview.project.project_code_name
        response = HttpResponse(apk, content_type='application/vnd.android.package-archive')
        response['Content-Disposition'] = 'attachment; filename=%s.apk' % file_name

        return response
