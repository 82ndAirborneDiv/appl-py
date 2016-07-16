from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from wsgiref.util import FileWrapper
from django_user_agents.utils import get_user_agent
from operator import itemgetter
from .models import Project, Release, Description, Release, Screenshot
from .create_manifest import write_manifest_send


@login_required()
def home_page(request):
    request.session['platform'] = ''
    featured_releases = Release.objects.featured_releases()
    return render(request, 'apps/home.html', {'featured_releases': featured_releases})


def login(request):
    return render(request, 'admin/login.html')


@login_required()
def app_release(request, platform, release_id):

    request.session['platform'] = platform.lower()
    group_size = 4
    history_limit = 6

    selected_release = Release.objects.select_related('project', 'description', 'icon').get(id=release_id)
    latest_releases = Release.objects.exclude(id=release_id).latest_releases(selected_release.project,
                                                                             selected_release.platform,
                                                                             history_limit)
    screenshots = selected_release.screenshots.all()

    return render(request, 'apps/app-release-page.html', {
        'release': selected_release,
        'latest_releases': latest_releases,
        'project': selected_release.project,
        'description': selected_release.description,
        'icon': selected_release.icon,
        'screenshotGroups4': [screenshots[i:i + group_size] for i in range(0, len(screenshots), group_size)],
        'screenshotGroups3': [screenshots[i:i + 3] for i in range(0, len(screenshots), 3)],
        'screenshotGroups2': [screenshots[i:i + 2] for i in range(0, len(screenshots), 2)],
        'screenshotGroups1': [screenshots[i:i + 1] for i in range(0, len(screenshots), 1)],
    })


# platform_page should display only the latest,
# non-archived release for the respective platform for each non-archived project.
@login_required()
def platform_page(request, platform, sortfield=None):
    request.session['platform'] = platform.lower()
    platform_releases = []

    # iterate through each project and get latest release
    for project in Project.objects.active_projects_by_platform_string(platform):
        latest_release = Release.objects.latest_release(project, project.platform)
        platform_releases.append(latest_release)

    if sortfield and sortfield.lower == 'sortname':
        platform_releases.sort(key=lambda x: x.project.title, reverse=False)
    else:
        platform_releases.sort(key=lambda x: x.release_date, reverse=False)

    return render(request, 'apps/platform-page.html', {'platform': platform, 'platform_releases': platform_releases})


@login_required()
def app_download(request, platform, release_id):
    user_agent = get_user_agent(request)
    release = Release.objects.select_related('project').get(id=release_id)
    app_file = release.app_file
    file_name = release.project.code_name

    if str.lower(platform) == "ios":
        ipa_file_url = request.build_absolute_uri(app_file.url)
        if user_agent.os.family == "iOS":
            response = write_manifest_send(request, release, ipa_file_url)
            return response
        else:
            response = HttpResponse(FileWrapper(app_file), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=%s.ipa' % file_name
            return response

    elif str.lower(platform) == "android":
        response = HttpResponse(app_file, content_type='application/vnd.android.package-archive')
        response['Content-Disposition'] = 'attachment; filename=%s.apk' % file_name
        return response
