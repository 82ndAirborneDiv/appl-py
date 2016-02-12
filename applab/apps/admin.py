from django.contrib import admin

from .models import Project,ProjectOverview,ProjectOverviewScreenshot,AndroidProject,IosProject
applabModels = [Project,ProjectOverview,ProjectOverviewScreenshot,AndroidProject,IosProject]
admin.site.register(applabModels)
