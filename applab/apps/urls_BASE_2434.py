from django.conf.urls import url
from apps import views

urlpatterns = [
<<<<<<< Temporary merge branch 1
    url(r'^$', views.hello_world, name='hello_world'),
    url(r'^login/$', views.login, name='login'),
    url(r'^applab/$', views.home, name='applab_home'),
    url(r'^applab/ios/', views.ios, name='applab_ios'),
    url(r'^applab/android/', views.android, name='applab_android'),
    url(r'^applab/app/(?P<app_id>\d+)/', views.app_detail,name = 'app_detail')
]
=======
    url(r'^$', views.home_page, name='home_page'),
]


>>>>>>> Temporary merge branch 2
