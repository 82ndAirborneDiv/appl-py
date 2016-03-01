from django.conf.urls import url
from apps import views

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^(?P<platform>[a-zA-Z]+)/$', views.platform_page, name='platform_page'),
    url(r'^(?P<platform>[a-zA-Z]+)/(?P<release_id>[0-9\-]+)/$', views.app_page, name='app_page'),
    #url(r'^applab/ios/$', views.ios_page, name='ios_page'),
    #url(r'^applab/android/$', views.android_page, name='android_page'),
    #url(r'^applab/app_release_project/(?P<codename>[a-z A-Z 0-9\-]+)/$', views.project_page, name = 'app_release_project')
]


