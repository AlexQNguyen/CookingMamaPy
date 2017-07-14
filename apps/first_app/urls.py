from django.conf.urls import url
from . import views

urlpatterns = [
url(r'^$', views.index),
url(r'^dashboard$', views.show),
url(r'^add_user$', views.add_user),
url(r'^login$', views.login),
url(r'^recipe$', views.recipe),
url(r'^add_recipe$', views.add_recipe),
url(r'^delete/(?P<id>\d+)$', views.delete)


]
