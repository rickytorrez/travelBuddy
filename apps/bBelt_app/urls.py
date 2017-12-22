from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index), 
    url(r'^register$', views.register), 
    url(r'^login$', views.login), 
    url(r'^logout$', views.logout),
    url(r'^home$', views.home),
    url(r'^add$', views.add),
    url(r'^add_travel$', views.add_travel),
    url(r'^join/(?P<other_id>\d+)$', views.join),
    url(r'^trip/(?P<id>\d+)$', views.trip),
    url(r'^remove/(?P<id>\d+)$', views.remove),
]