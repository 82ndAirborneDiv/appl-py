from django.contrib import admin

# Register your models here.
from .models import Project, ProjectOverview, ProjectOverviewScreenshot
from .models import IosProject, IosRelease, AndroidProject, AndroidRelease

admin.site.register(Project)


class ProjectOverviewScreenshotInline(admin.TabularInline):
    model = ProjectOverviewScreenshot
    readonly_fields = ('screenshot_image',)
    fields = ('screenshot_image', 'screenshot')


class ProjectOverviewAdmin(admin.ModelAdmin):
    readonly_fields = ('date_published', 'icon_image')
    fields = ('project', 'date_published', 'description', 'icon_image', 'icon')
    list_filter = ['date_published', 'description']
    inlines = [ProjectOverviewScreenshotInline]

admin.site.register(ProjectOverview, ProjectOverviewAdmin)
admin.site.register(ProjectOverviewScreenshot)
admin.site.register(IosProject)
admin.site.register(IosRelease)
admin.site.register(AndroidProject)
admin.site.register(AndroidRelease)


