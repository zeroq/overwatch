# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from django.urls import include, path
from ow_clients import views


app_name = 'owclients'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_client, name='create_client'),
    path('<hostname>/delete/', views.delete_client, name='delete_client'),
    path('<hostname>/deploy/', views.deploy, name='deploy'),
    path('<hostname>/<scanid>/list/', views.view_scan_results, name='view_scan_results'),
    path('<hostname>/get/rkhunter/', views.get_rkhunter, name='get_rkhunter'),
]
