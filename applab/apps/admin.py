from django.contrib import admin

# Register your models here.
from .models import Project, ProjectOverview, ProjectScreenshot, IosProject, IosRelease

admin.site.register(Project)
admin.site.register(ProjectOverview)
admin.site.register(ProjectScreenshot)
admin.site.register(IosProject)
admin.site.register(IosRelease)


