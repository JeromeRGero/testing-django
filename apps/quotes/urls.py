from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'reg$', views.reg),
    url(r'logout$', views.logout),
    url(r'login$', views.login),
    url(r'quotes$', views.quotes),
    url(r'add$', views.adding),
    url(r'addfav/(?P<num>\d+)$', views.addfav),
    url(r'^delete/(?P<num>\d+)$', views.unfavorite),
    url(r'user/(?P<num>\d+)$', views.userpage),
    # url(r'^books/submit/(?P<num>\d+)$', views.submitreview),
]