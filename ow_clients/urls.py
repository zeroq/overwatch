# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from django.urls import include, path
from ow_clients import views


app_name = 'owclients'
urlpatterns = [
    path('', views.index, name='index'),
    path('<hostname>/deploy/', views.deploy, name='deploy'),
    path('<hostname>/get/rkhunter/', views.get_rkhunter, name='get_rkhunter'),
]
