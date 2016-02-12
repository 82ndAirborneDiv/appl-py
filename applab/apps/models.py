from django.db import models
from django.utils.timezone import localtime
from django.utils.html import mark_safe


class Project(models.Model):
    """ The ProjectTitle is the top level object for all apps and is a foreign key for all ProjectOverview objects. """
    title = models.CharField(max_length=200)
    project_code_name = models.SlugField(max_length=30)    # the code name used to refer to the project, e.g. lydia
    is_archived = models.BooleanField(default=False)       # archived projects will not be listed with active projects

    def __str__(self):
        return self.title


class ProjectOverview(models.Model):
    """ A ProjectOverview object belongs to a Project and contains text description, an icon, and has multiple screenshots
    as it is a foreign key to the ProjectScreenshot object. The attributes of this object may evolve over time and are
    separated from the Project object
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField()
    icon = models.ImageField()
    date_published = models.DateTimeField(auto_now=True)
    source_code_link = models.URLField()

    def __str__(self):
        return str(localtime(self.date_published).strftime('%Y-%m-%d %I:%M %p'))


class ProjectOverviewScreenshot(models.Model):
    """ This object is a screenshot of the app, each ProjectAssets object can have multiple screenshots
    """
    project_overview = models.ForeignKey(ProjectOverview, related_name='screenshots')
    screenshot = models.ImageField()

    def admin_image(self):
        return mark_safe('<img src="%s" style="max-height: 100px; max-width: 100px;" />' % self.screenshot.url)
    admin_image.allow_tags = True

    def __str__(self):
        return self.screenshot.path


class IosProject(models.Model):
    project_overview = models.ForeignKey(ProjectOverview, on_delete=models.CASCADE)
    bundle_id = models.CharField(max_length=50)
    apple_app_store_link = models.URLField()

    def __str__(self):
        return self.bundle_id


class AndroidProject(models.Model):
    project_overview = models.ForeignKey(ProjectOverview, on_delete=models.CASCADE)
    google_play_link = models.URLField()


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

    def __str__(self):
        return '%d.%d.%d.%d' % (self.major_version, self.minor_version, self.point_version, self.build_version)


class IosRelease(Release):
    ios_project = models.ForeignKey(IosProject, on_delete=models.CASCADE)
    ipa_file = models.FileField()
    manifest_file = models.FileField()


class AndroidRelease(Release):
    android_project = models.ForeignKey(AndroidProject, on_delete=models.CASCADE)
    apk_file = models.FileField()


