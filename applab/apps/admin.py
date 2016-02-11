from django.contrib import admin

# Register your models here.
from .models import ProjectTitle, ProjectOverview, ProjectScreenshot, IosProject, IosRelease

admin.site.register(ProjectTitle)
admin.site.register(ProjectOverview)
admin.site.register(ProjectScreenshot)
admin.site.register(IosProject)
admin.site.register(IosRelease)


