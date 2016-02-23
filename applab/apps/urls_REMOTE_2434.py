from django.conf.urls import url
from apps import views

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^applab/app_release/(?P<release>[a-zA-Z0-9\-]+)/$',views.app_page,name='app_page'),
    url(r'^applab/app_release_project/(?P<codename>[a-z A-Z 0-9\-]+)/$', views.project_page, name = 'app_release_project')
]


