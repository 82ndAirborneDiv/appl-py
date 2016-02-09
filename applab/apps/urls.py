from django.conf.urls import url
from apps import views

urlpatterns = [
    url(r'^$', views.hello_world, name='hello_world'),
    url(r'^login/$', views.login, name='login'),
    url(r'^applab/$', views.home, name='applab_home'),
    url(r'^applab/ios/', views.ios, name='applab_ios'),
    url(r'^applab/android/', views.android, name='applab_android')
]