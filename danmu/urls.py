# chat/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
    # url(r'^(?P<room_name>[^/]+)/analyse$', views.analyse, name='analyse'),
    # url(r'^(?P<room_name>[^/]+)/jiebaanalyse$', views.jiebaanalyse, name='jiebaanalyse')
    url(r'^$', views.room, name='room'),
    url(r'^analyse$', views.analyse, name='analyse'),
    url(r'^jiebaanalyse$', views.jiebaanalyse, name='jiebaanalyse'),
    url(r'^suspectuser$', views.suspectuser, name='suspectuser'),
    url(r'^login$', views.analyse, name='analyse'),
    url(r'^suggestban', views.suggestban, name='suggestban'),
]