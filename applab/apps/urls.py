from django.conf.urls import url
from apps import views

urlpatterns = [
    url(r'^$', views.hello_world, name='hello_world'),
    url(r'^login/$', views.login, name='login'),
]


