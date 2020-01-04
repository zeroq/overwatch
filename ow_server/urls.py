# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from django.urls import include, path
from ow_server import views


app_name = 'owservers'
urlpatterns = [
    path('', views.index, name='index'),
    path('edit/', views.edit_server, name='edit_server'),
]
