from django.conf.urls import url
from apps import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^home/$', views.home, name='applab_home'),
    url(r'^$', views.home_page, name='home_page'),
    url(r'^applab/$', views.home, name='applab_home'),
    url(r'^applab/ios/', views.ios, name='applab_ios'),
    url(r'^applab/android/', views.android, name='applab_android'),
    url(r'^applab/app/(?P<app_id>\d+)/', views.app_detail,name = 'app_detail')
    url(r'^applab/app_release/(?P<release>[a-zA-Z0-9\-]+)/$',views.app_page,name='app_page'),
    url(r'^applab/app_release_project/(?P<codename>[a-z A-Z 0-9\-]+)/$', views.project_page, name = 'app_release_project')
]
