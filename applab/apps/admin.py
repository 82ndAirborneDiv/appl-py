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
    fieldsets = [
        (None,              {'fields': ['project','date_published', 'description']}),
        ('Version Info',   {'fields': ['major_version', 'minor_version']}),
        ('Icon',   {'fields': ['icon_image', 'icon']}),
        ('Source Code Link',   {'fields': ['source_code_link']})
    ]

    list_filter = ['date_published', 'description']
    inlines = [ProjectOverviewScreenshotInline]


admin.site.register(ProjectOverview, ProjectOverviewAdmin)
admin.site.register(ProjectOverviewScreenshot)
admin.site.register(IosProject)
admin.site.register(IosRelease)
admin.site.register(AndroidProject)
admin.site.register(AndroidRelease)


