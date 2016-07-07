from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from wsgiref.util import FileWrapper
from django_user_agents.utils import get_user_agent
from operator import itemgetter
from collections import OrderedDict
from .models import Project, IosRelease, AndroidRelease, ProjectOverviewScreenshot, Release
from .create_manifest import write_manifest_send


@login_required()
def home_page(request):
    request.session['platform'] = ''
    featured_releases = {}

    # iterate through each active project to set the apps which will be passed to the template.
    for project in Project.objects.filter(is_archived=False):
        android_releases = AndroidRelease.objects \
            .filter(android_project__project_overview__project_id=project.id,
                    is_featured_release=True)

        for android_release in android_releases:
            if android_release.is_featured_release:
                featured_releases[android_release.timestamp] = {'overview': android_release.android_project.project_overview,
                                                                'release': android_release}

        ios_releases = IosRelease.objects \
            .filter(ios_project__project_overview__project_id=project.id,
                    is_featured_release=True)

        for ios_release in ios_releases:
                if ios_release.is_featured_release:
                    featured_releases[ios_release.timestamp] = {'overview': ios_release.ios_project.project_overview,
                                                                'release': ios_release}
    sorted_featured_releases = OrderedDict(sorted(featured_releases.items(), reverse=True))

    return render(request, 'apps/home.html', {'featured_releases': sorted_featured_releases})


def home_page_old(request):
    request.session['platform'] = ''
    apps_to_display = []

    # Get all non-archived project objects.
    avail_apps = Project.objects.filter(is_archived=False)

    # Iterate through each project to set the apps which will be passed to the template.
    for app in avail_apps:
        one_app = {'title': app.title}
        try:
            release = AndroidRelease.objects \
                .filter(android_project__project_overview__project_id=app.id,
                        is_archived=False,
                        is_featured_release=True) \
                .order_by('-major_version', '-minor_version', '-point_version', '-build_version')[0]
            one_app['platform'] = 'android'
            one_app['releaseDate'] = release.timestamp
            one_app['releaseVersion'] = '{0}.{1}.{2}.{3}'.format(release.major_version, release.minor_version,
                                                                 release.point_version, release.build_version)
            one_app['id'] = release.id
            one_app['description'] = release.android_project.project_overview.description
            one_app['icon'] = release.android_project.project_overview.icon
            apps_to_display.append(one_app)
        except IndexError or AndroidRelease.DoesNotExist:
            pass
        try:
            release = IosRelease.objects \
                .filter(ios_project__project_overview__project_id=app.id,
                        is_archived=False,
                        is_featured_release=True) \
                .order_by('-major_version', '-minor_version', '-point_version', '-build_version')[0]
            one_app['platform'] = 'ios'
            one_app['releaseDate'] = release.timestamp
            one_app['releaseVersion'] = '{0}.{1}.{2}.{3}'.format(release.major_version, release.minor_version,
                                                                 release.point_version, release.build_version)
            one_app['id'] = release.id
            one_app['description'] = release.ios_project.project_overview.description
            one_app['icon'] = release.ios_project.project_overview.icon
            apps_to_display.append(one_app)
        except IndexError or IosRelease.DoesNotExist:
            pass
    sort = sorted(apps_to_display, key=itemgetter('releaseDate'), reverse=True)
    apps_to_display = sort
    return render(request, 'apps/home.html', {'apps': apps_to_display})


def login(request):
    return render(request, 'admin/login.html')



@login_required()
def app_release(request, platform, release_id):
    request.session['platform'] = platform.lower()
    group_size = 4
    history_limit = 6

    if platform == 'ios':
        cur_release = IosRelease.objects \
            .select_related('ios_project__project_overview__project') \
            .filter(id=release_id, is_archived=False)[0]
        overview = cur_release.ios_project.project_overview

        # previous releases should consider all releases for overall Project
        previous_releases = IosRelease.objects \
            .select_related('ios_project__project_overview__project') \
            .filter(is_archived=False,
                    ios_project__project_overview__project_id=cur_release.ios_project.project_overview.project.id) \
            .exclude(id=cur_release.id) \
            .order_by('-major_version', '-minor_version', '-point_version', '-build_version')[:history_limit+1]

        # get latest, non-archived, release, NOT filtered by featured release
        latest_release = IosRelease.objects \
            .filter(ios_project__project_overview__project_id=overview.project.id,
                    is_archived=False) \
            .order_by('-major_version', '-minor_version', '-point_version', '-build_version')[0]

    elif platform == 'android':
        cur_release = AndroidRelease.objects \
            .select_related('android_project__project_overview__project') \
            .filter(id=release_id, is_archived=False)[0]
        overview = cur_release.android_project.project_overview

        # previous releases should consider all releases for overall Project
        previous_releases = AndroidRelease.objects \
            .select_related('android_project__project_overview__project') \
            .filter(is_archived=False,
                    android_project__project_overview__project_id=cur_release.android_project.project_overview.project.id) \
            .exclude(id=cur_release.id) \
            .order_by('-major_version', '-minor_version', '-point_version', '-build_version')[:history_limit+1]

        # get latest, non-archived, release, NOT filtered by featured release
        latest_release = AndroidRelease.objects \
            .filter(android_project__project_overview__project_id=overview.project.id, is_archived=False) \
            .order_by('-major_version', '-minor_version', '-point_version', '-build_version')[0]

    screenshots = ProjectOverviewScreenshot.objects.filter(project_overview=overview.id)
    app_detail = {
        'overview': overview,
        'currentRelease': cur_release,
        'previousReleases': previous_releases,
        'latestRelease': latest_release,
        'screenshotGroups4': [screenshots[i:i + group_size] for i in range(0, len(screenshots), group_size)],
        'screenshotGroups3': [screenshots[i:i + 3] for i in range(0, len(screenshots), 3)],
        'screenshotGroups2': [screenshots[i:i + 2] for i in range(0, len(screenshots), 2)],
        'screenshotGroups1': [screenshots[i:i + 1] for i in range(0, len(screenshots), 1)],
        'title': overview.project.title,
        'platform': platform,
        'releaseVersion': '{0}.{1}.{2}.{3}'.format(cur_release.major_version, cur_release.minor_version,
                                                   cur_release.point_version, cur_release.build_version),
        'latestVersion': '{0}.{1}.{2}.{3}'.format(latest_release.major_version, latest_release.minor_version,
                                                  latest_release.point_version, latest_release.build_version),
    }
    if str.lower(platform) == 'android':
        app_detail['app_identifier'] = cur_release.android_project.application_id
    elif str.lower(platform) == 'ios':
        app_detail['app_identifier'] = cur_release.ios_project.bundle_id

    return render(request, 'apps/app-release-page.html', {'appDetail': app_detail})


# platform_page should display only the latest,
# non-archived release for the respective platform for each non-archived project.
@login_required()
def platform_page(request, platform, sortfield=None):
    request.session['platform'] = platform.lower()

    platform_app = {'platform': platform, 'apps': []}

    # Get all non-archived project objects.
    avail_apps = Project.objects.filter(is_archived=False)

    # Iterate through each project to set the apps which will be passed to the template.
    for app in avail_apps:
        one_app = {}
        one_app['title'] = app.title
        if str.lower(platform) == 'android':
            try:
                # Select latest release, not filtered_by_featured for current project,
                # append to dictionary to pass to template.
                release = AndroidRelease.objects \
                    .filter(android_project__project_overview__project_id=app.id,
                            is_archived=False) \
                    .order_by('-major_version', '-minor_version', '-point_version', '-build_version')[0]
                one_app['platform'] = 'android'
                one_app['releaseDate'] = release.timestamp
                one_app['releaseVersion'] = '{0}.{1}.{2}.{3}'.format(release.major_version, release.minor_version,
                                                                     release.point_version, release.build_version)
                one_app['id'] = release.id
                one_app['description'] = release.android_project.project_overview.description
                one_app['icon'] = release.android_project.project_overview.icon
                platform_app['apps'].append(one_app)
            except IndexError:
                pass
        elif str.lower(platform) == 'ios':
            try:
                # Select latest release, not filtered_by_featured for current project,
                # append to dictionary to pass to template.
                release = IosRelease.objects \
                    .filter(ios_project__project_overview__project_id=app.id, is_archived=False) \
                    .order_by('-major_version', '-minor_version', '-point_version', '-build_version')[0]
                one_app['platform'] = 'ios'
                one_app['releaseDate'] = release.timestamp
                one_app['releaseVersion'] = '{0}.{1}.{2}.{3}'.format(release.major_version, release.minor_version,
                                                                     release.point_version, release.build_version)
                one_app['id'] = release.id
                one_app['description'] = release.ios_project.project_overview.description
                one_app['icon'] = release.ios_project.project_overview.icon
                platform_app['apps'].append(one_app)
            except IndexError:
                pass

    if sortfield:
        sortfield = sortfield.lower()
        if sortfield == 'sortname':
            sort = sorted(platform_app['apps'], key=itemgetter('title'))
            platform_app['apps'] = sort
        if sortfield == 'sortnamedesc':
            sortfield = '-' + platform + '_project__project_overview__project__title'
        elif sortfield == 'sortreleasedate':
            sort = sorted(platform_app['apps'], key=itemgetter('releaseDate'), reverse=True)
            platform_app['apps'] = sort
    else:
        sort = sorted(platform_app['apps'], key=itemgetter('releaseDate'), reverse=True)
        platform_app['apps'] = sort

    return render(request, 'apps/platform-page.html', {'platform_app': platform_app})


@login_required()
def app_download(request, platform, release_id):
    user_agent = get_user_agent(request)
    if str.lower(platform) == "ios":
        app = IosRelease.objects \
            .select_related('ios_project__project_overview__project') \
            .filter(id=release_id)[0]
        ipa_file_url = request.build_absolute_uri(app.ipa_file.url)
        if user_agent.os.family == "iOS":
            response = write_manifest_send(request, app, ipa_file_url)
            return response
        else:
            file_name = app.ios_project.project_overview.project.project_code_name
            ipa_file = app.ipa_file
            response = HttpResponse(FileWrapper(ipa_file), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=%s.ipa' % file_name

            return response

    elif str.lower(platform) == "android":
        app = AndroidRelease.objects \
            .select_related('android_project__project_overview__project') \
            .filter(id=release_id)[0]

        apk = app.apk_file
        file_name = app.android_project.project_overview.project.project_code_name
        response = HttpResponse(apk, content_type='application/vnd.android.package-archive')
        response['Content-Disposition'] = 'attachment; filename=%s.apk' % file_name

        return response
