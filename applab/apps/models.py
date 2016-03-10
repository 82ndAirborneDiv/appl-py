from django.db import models
from django.utils.timezone import localtime
from django.utils.html import mark_safe
from applab.settings import MEDIA_ROOT

import os.path


class Project(models.Model):
    """ The ProjectTitle is the top level object for all apps and is a foreign key for all ProjectOverview objects. """
    title = models.CharField(max_length=200)
    project_code_name = models.SlugField(max_length=30)    # the code name used to refer to the project, e.g. lydia
    is_archived = models.BooleanField(default=False)       # archived projects will not be listed with active projects

    def __str__(self):
        return self.title


def overview_icon_upload_path(instance, filename):
    date_created = str(localtime(instance.date_published).strftime('%Y-%m-%d_%I-%M_%p'))
    return os.path.join(instance.project.project_code_name, date_created, "icons", filename)


class ProjectOverview(models.Model):
    """ A ProjectOverview object belongs to a Project and contains text description, an icon, and has multiple screenshots
    as it is a foreign key to the ProjectScreenshot object. The attributes of this object may evolve over time and are
    separated from the Project object
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    major_version = models.PositiveSmallIntegerField()
    minor_version = models.PositiveSmallIntegerField()
    date_published = models.DateTimeField(auto_now=True)
    description = models.TextField()
    icon = models.ImageField(upload_to=overview_icon_upload_path)
    source_code_link = models.URLField()

    def icon_image(self):
        return mark_safe('<img src="%s" style="max-height: 100px; max-width: 100px;" />' % self.icon.url)
    icon_image.allow_tags = True

    def __str__(self):
        return '%s %d.%d' % (self.project.title, self.major_version, self.minor_version)


def overview_screenshot_upload_path(instance, filename):
    date_created = str(localtime(instance.project_overview.date_published).strftime('%Y-%m-%d_%I-%M_%p'))
    return os.path.join(instance.project_overview.project.project_code_name, date_created, "screenshots", filename)


class ProjectOverviewScreenshot(models.Model):
    """ This object is a screenshot of the app, each ProjectAssets object can have multiple screenshots
    """
    project_overview = models.ForeignKey(ProjectOverview, related_name='screenshots')
    screenshot = models.ImageField(upload_to=overview_screenshot_upload_path)

    def screenshot_image(self):
        return mark_safe('<img src="%s" style="max-height: 100px; max-width: 100px;" />' % self.screenshot.url)
    screenshot_image.allow_tags = True

    def __str__(self):
        return self.screenshot.path


class IosProject(models.Model):
    project_overview = models.ForeignKey(ProjectOverview, on_delete=models.CASCADE)
    bundle_id = models.CharField(max_length=50)
    apple_app_store_link = models.URLField()

    def __str__(self):
        return '%s' % self.project_overview.project.title


class AndroidProject(models.Model):
    project_overview = models.ForeignKey(ProjectOverview, on_delete=models.CASCADE)
    google_play_link = models.URLField()

    def __str__(self):
        return '%s' % self.project_overview.project.title


class Release(models.Model):
    """ A Release belongs to a Project and contains a version number and a is_archived flag.
    A Release is a foreign key for ReleaseAssets and ReleaseApp """
    major_version = models.PositiveSmallIntegerField()
    minor_version = models.PositiveSmallIntegerField()
    point_version = models.PositiveSmallIntegerField()
    build_version = models.PositiveSmallIntegerField()
    is_archived = models.BooleanField(default=False)
    what_is_new = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    is_featured_release = models.BooleanField(default=False)

    def __str__(self):
        return '%d.%d.%d.%d' % (self.major_version, self.minor_version, self.point_version, self.build_version)


def ipa_upload_path(instance, filename):
    version_path = '%d.%d.%d.%d' % (instance.major_version, instance.minor_version, instance.point_version, instance.build_version)
    platform_path = 'ios'
    return os.path.join(instance.ios_project.project_overview.project.project_code_name, platform_path, version_path, filename)


class IosRelease(Release):
    ios_project = models.ForeignKey(IosProject, on_delete=models.CASCADE)
    ipa_file = models.FileField(upload_to=ipa_upload_path)
    manifest_file = models.FileField(upload_to=ipa_upload_path)

    def __str__(self):
        return '%s %d.%d.%d.%d' % (self.ios_project.project_overview.project.title, self.major_version, self.minor_version, self.point_version, self.build_version)


def apk_upload_path(instance, filename):
    version_path = '%d.%d.%d.%d' % (instance.major_version, instance.minor_version, instance.point_version, instance.build_version)
    platform_path = 'android'
    return os.path.join(instance.android_project.project_overview.project.project_code_name, platform_path, version_path, filename)


class AndroidRelease(Release):
    android_project = models.ForeignKey(AndroidProject, on_delete=models.CASCADE)
    apk_file = models.FileField(upload_to=apk_upload_path)

    def __str__(self):
        return '%s %d.%d.%d.%d' % (self.android_project.project_overview.project.title, self.major_version, self.minor_version, self.point_version, self.build_version)



