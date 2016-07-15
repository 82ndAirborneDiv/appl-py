from django.contrib import admin

# Register your models here.
from .models import Project, Description, Screenshot, Release, Icon


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'code_name', 'is_archived']}),
        ('Platforms Supported', {'fields': ['platform']}),
        ('iOS Info', {'fields': ['apple_app_store_link', 'bundle_id']}),
        ('Android Info', {'fields': ['application_id', 'google_play_link']})
    ]


class ReleaseScreenshotAdmin(admin.ModelAdmin):
    model = Screenshot
    readonly_fields = ('screenshot_image',)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Release)
admin.site.register(Screenshot, ReleaseScreenshotAdmin)
admin.site.register(Icon)
admin.site.register(Description)

