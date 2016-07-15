from django.db import models
from django.utils.timezone import localtime
from django.utils.html import mark_safe
from applab.settings import MEDIA_ROOT

import os.path


class Platform(models.Model):
    class Meta:
        abstract = True

    NO_PLATFORM = ''
    IOS = 'ios'
    ANDROID = 'and'
    WINDOWS = 'win'
    CROSS_PLATFORM = 'crp'
    PLATFORM_CHOICES = (
        (NO_PLATFORM, 'No Platform'),
        (IOS, 'iOS'),
        (ANDROID, 'Android'),
        (WINDOWS, 'Windows Mobile'),
        (CROSS_PLATFORM, 'Cross-platform')
    )

    platform = models.CharField(max_length=3, choices=PLATFORM_CHOICES, default=NO_PLATFORM)

    def is_ios(self):
        return self.platform in self.IOS

    def is_android(self):
        return self.platform in self.ANDROID

    def is_windows(self):
        return self.platform in self.WINDOWS

    def is_cross_platform(self):
        return self.platform in self.CROSS_PLATFORM

    def platform_readable_name(self):
        for choice in self.PLATFORM_CHOICES:
            if choice[0] == self.platform:
                return choice[1]
        return ''

    def path_part_for_platform(self):
        if self.is_android():
            return 'android'
        elif self.is_ios():
            return 'ios'
        elif self.is_windows():
            return 'windows'
        elif self.is_cross_platform():
            return 'cross-platform'
        return 'other'


def platform_from_string(platform_text):
    platform = platform_text.lower()
    if platform == 'ios':
        return Platform.IOS
    elif platform == 'android':
        return Platform.ANDROID
    elif platform == 'windows':
        return Platform.WINDOWS
    return Platform.NO_PLATFORM


class ProjectQuerySet(models.QuerySet):
    def active_projects(self):
        return self.filter(is_archived=False)

    def active_projects_by_platform_string(self, platform_string):
        platform = platform_from_string(platform_string)
        return self.filter(is_archived=False, platform=platform)


class Project(Platform):
    """ The Project is the top level object for all apps and is a foreign key for all ProjectOverview objects. """
    title = models.CharField(max_length=200)
    code_name = models.SlugField(max_length=30)    # the code name used to refer to the project, e.g. lydia
    is_archived = models.BooleanField(default=False)       # archived projects will not be listed with active projects
    source_code_link = models.URLField(blank=True, max_length=200, default="")

    # iOS project attributes
    apple_app_store_link = models.URLField(blank=True, max_length=200, default="")
    bundle_id = models.CharField(max_length=100, blank=True, default="")

    # Android project attributes
    application_id = models.CharField(max_length=100, blank=True, default="")
    google_play_link = models.URLField( max_length=200, blank=True, default="")

    objects = ProjectQuerySet.as_manager()

    def __str__(self):
        return self.title


class AppAssetVersion(Platform):
    """ The AppAssetVersion class is an abstract base class for assets associated with an app. Assets are icons,
    screenshots, and descriptions and this class defines what version of the app they apply to and defines the path
    to any assest files such as images for icons and screenshots.
    """

    class Meta:
        abstract = True
    applies_to_major_version = models.PositiveSmallIntegerField()
    applies_to_minor_version = models.PositiveSmallIntegerField()

    def get_version_string(self):
        return "{}.{}".format(self.applies_to_major_version, self.applies_to_minor_version)

    def root_path(self):
        return os.path.join(self.project.code_name, 'assets', self.path_part_for_platform())

    def icon_path(self):
        return os.path.join(self.root_path(), 'icons', self.get_version_string())

    def screenshot_path(self):
        return os.path.join(self.root_path(), 'screenshots', self.get_version_string())


def get_screenshot_path(instance, filename):
    return os.path.join(instance.screenshot_path(), filename)


def get_icon_path(instance, filename):
    return os.path.join(instance.icon_path(), filename)


class Description(AppAssetVersion):
    """ A ReleaseDescription object belongs to a Project and contains high level text description of one or more
    releases.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s, %s, %s' % (self.project.title, self.platform_readable_name(), self.get_version_string())


class Icon(AppAssetVersion):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_icon_path)
    date_added = models.DateTimeField(auto_now=True)

    def icon_image(self):
        return mark_safe('<img src="%s" style="max-height: 100px; max-width: 100px;" />' % self.image.url)
    icon_image.allow_tags = True

    def __str__(self):
        return "{} Version {} for {}".format(os.path.basename(self.image.name), self.get_version_string(), self.platform_readable_name())


class Screenshot(AppAssetVersion):
    """ This class represents a screenshot of a group of versions of the app. The version numbering for screenshots
    are defined in the base class AppAssetVersion. The path to the image file that represents the screenshot is in the
    base class as well.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def screenshot_image(self):
        return mark_safe('<img src="%s" style="max-height: 100px; max-width: 100px;" />' % self.image.url)
    screenshot_image.allow_tags = True
    image = models.ImageField(upload_to=get_screenshot_path)

    def __str__(self):
        return "{} Version {} for {}".format(os.path.basename(self.image.name), self.get_version_string(), self.platform_readable_name())


class ReleaseQuerySet(models.QuerySet):

    def by_project_platform(self, project, platform):
        return self.filter(project=project, platform=platform)

    def latest_releases(self, project, platform, count):
        return self.filter(project=project, platform=platform).order_by('-major_version', '-minor_version',
                                                                        '-point_version', '-build_version')[:count]

    def featured_releases(self):
        return self.filter(is_featured=True)


class Release(Platform):
    """ A Release belongs to a Project and contains a version number and a is_archived flag.
    A Release is a foreign key for ReleaseAssets and ReleaseApp """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.ForeignKey(Description)
    icon = models.ForeignKey(Icon)
    screenshots = models.ManyToManyField(Screenshot)
    major_version = models.PositiveSmallIntegerField()
    minor_version = models.PositiveSmallIntegerField()
    point_version = models.PositiveSmallIntegerField()
    build_version = models.PositiveSmallIntegerField()
    is_archived = models.BooleanField(default=False)
    what_is_new = models.TextField()
    release_date = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    def version_string(self):
        return '{}.{}.{}.{}'.format(self.major_version, self.minor_version, self.point_version, self.build_version)

    def app_upload_path(self, filename):
        return os.path.join(self.project.code_name, 'apps', self.path_part_for_platform(),
                            self.version_string(), filename)

    app_file = models.FileField(upload_to=app_upload_path)

    def __str__(self):
        return '{} {}'.format(self.project.title, self.version_string())

    class Meta:
        ordering = ('release_date',)

    objects = ReleaseQuerySet.as_manager()




