from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^login$', views.login),
    url(r'^home$', views.home),
    url(r'^logout$', views.logout),
    url(r'^new_activity$', views.new_activity),
    url(r'^activity/(?P<act_id>\d+)/$', views.activity),
    url(r'^delete/(?P<act_id>\d+)/$', views.delete),
    url(r'^join/(?P<act_id>\d+)/$', views.join),
    url(r'^leave/(?P<act_id>\d+)/$', views.leave),
    url(r'^new$', views.new),
]
