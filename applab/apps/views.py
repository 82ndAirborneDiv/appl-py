from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectOverview

@login_required()
def home_page(request):
    apps_to_display = ProjectOverview.objects.filter(project__in=Project.objects.filter(is_archived=False).order_by('title'))

    return render(request, 'applab/home.html', {'apps': apps_to_display})

def login(request):
    return render(request, 'applab/templates/registration/login.html')
