# chat/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
    # url(r'^(?P<room_name>[^/]+)/analyse$', views.analyse, name='analyse'),
    # url(r'^(?P<room_name>[^/]+)/jiebaanalyse$', views.jiebaanalyse, name='jiebaanalyse')
    url(r'^$', views.liveroominf, name='liveroominf'),
    url(r'nowtimeroomdata', views.nowtimeroomdata, name='nowtimeroomdata'),
    url(r'danmu_num_data', views.danmu_num_data, name='danmu_num_data'),
    url(r'pasttimeroomdata', views.pasttimeroomdata, name='pasttimeroomdata'),
    url(r'makecloudword', views.makecloudword, name='makecloudword'),
    url(r'userdata', views.userdata, name='userdata'),
    url(r'getDetailedInf', views.getDetailedInf, name='getDetailedInf'),
]