from django.conf.urls import url
from apps import views

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    #url(r'^applab/$', views.home_page, name='home_page'),
    url(r'^applab/app/(?P<project_title>[a-zA-Z0-9\-]+)/$',views.app_page,name='app_page'),
    url(r'^(?P<platform>[a-z A-Z]+)/(?P<sortfield>[a-z A-Z]+)/$', views.platform_page, name='platform_page'),
    url(r'^(?P<platform>[a-z A-Z]+)/$', views.platform_page, name='platform_page'),
    url(r'^(?P<platform>[a-z A-Z]+)/(?P<release_id>[0-9]+)/$', views.app_release, name='app_release_page'),
    #url(r'^applab/app_release_project/(?P<codename>[a-z A-Z 0-9\-]+)/$', views.project_page, name = 'app_release_project')
]


