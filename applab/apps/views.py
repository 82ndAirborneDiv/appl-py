from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectOverview

@login_required()
def home_page(request):
    projects_to_display = ProjectOverview.objects.filter(project__in=Project.objects.filter(is_archived=False).order_by('title'))
    projects_ordered = projects_to_display.order_by()

    return render(request, 'applab/home.html', {'projects': projects_to_display})

def login(request):
    return render(request, 'applab/templates/registration/login.html')
