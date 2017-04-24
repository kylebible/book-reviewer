from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^books$', views.books),
    url(r'^logout$', views.logout),
    url(r'^books/add$', views.addbookpage),
    url(r'^addbook$', views.addbook),
    url(r'^books/(?P<id>\d)+$', views.bookpage),
    url(r'^newreview/(?P<id>\d)+$', views.newreview),
    url(r'^user/(?P<id>\d)+$', views.userpage)
]
