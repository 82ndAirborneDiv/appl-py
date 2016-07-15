from django.contrib import admin

# Register your models here.
from .models import Project, Description, Screenshot, Release, Icon


class ReleaseScreenshotInline(admin.TabularInline):
    model = Release.screenshots.through


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'code_name', 'is_archived']}),
        ('Platforms Supported', {'fields': ['platform']}),
        ('iOS Info', {'fields': ['apple_app_store_link', 'bundle_id']}),
        ('Android Info', {'fields': ['application_id', 'google_play_link']})
    ]


class ReleaseAdmin(admin.ModelAdmin):
    inlines = [
        ReleaseScreenshotInline,
    ]

    exclude = ('screenshots',)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Release, ReleaseAdmin)
admin.site.register(Screenshot)
admin.site.register(Icon)
admin.site.register(Description)

