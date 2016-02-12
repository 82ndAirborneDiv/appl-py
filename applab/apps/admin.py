from django.contrib import admin

# Register your models here.
from .models import Project, ProjectOverview, ProjectOverviewScreenshot
from .models import IosProject, IosRelease, AndroidProject, AndroidRelease

admin.site.register(Project)


class ProjectOverviewScreenshotInline(admin.TabularInline):
    model = ProjectOverviewScreenshot
    readonly_fields = ('admin_image',)
    fields = ('admin_image',)


class ProjectOverviewAdmin(admin.ModelAdmin):
    readonly_fields = ('date_published',)
    fields = ('project', 'date_published', 'description','icon')
    list_filter = ['date_published', 'description']
    inlines = [ProjectOverviewScreenshotInline]

admin.site.register(ProjectOverview, ProjectOverviewAdmin)
admin.site.register(ProjectOverviewScreenshot)
admin.site.register(IosProject)
admin.site.register(IosRelease)
admin.site.register(AndroidProject)
admin.site.register(AndroidRelease)


