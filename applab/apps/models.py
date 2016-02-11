from django.db import models


class Project(models.Model):
    """ The ProjectTitle is the top level object for all apps and is a foreign key for all ProjectOverview objects. """
    title = models.CharField(max_length=200)
    project_code_name = models.SlugField(max_length=30)    # the code name used to refer to the project, e.g. lydia
    is_archived = models.BooleanField(default=False)       # archived projects will not be listed with active projects

    def __str__(self):
        return self.title


class ProjectScreenshot(models.Model):
    """ This object is a screenshot of the app, each ProjectAssets object can have multiple screenshots
    """
    screenshot = models.ImageField()


class ProjectOverview(models.Model):
    """ A ProjectOverview object belongs to a Project and contains text description, an icon, and has multiple screenshots
    as it is a foreign key to the ProjectScreenshot object. The attributes of this object may evolve over time and are
    separated from the Project object
    """
    project_title = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField()
    icon = models.ImageField()
    screenshots = models.ManyToManyField(ProjectScreenshot)
    timestamp = models.DateTimeField(auto_now=True)
    source_code_link = models.URLField()


class IosProject(models.Model):
    project_overview = models.ForeignKey(ProjectOverview, on_delete=models.CASCADE)
    bundle_id = models.CharField(max_length=50)
    apple_app_store_link = models.URLField()


class AndroidProject(models.Model):
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


class IosRelease(models.Model):
    release = models.ForeignKey(Release, on_delete=models.CASCADE)
    ipa_file = models.FileField()
    manifest_file = models.FileField()


class AndroidRelease(models.Model):
    release = models.ForeignKey(Release, on_delete=models.CASCADE)
    apk_file = models.FileField()


