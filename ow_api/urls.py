# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from django.urls import include, path
from ow_api import views


app_name = 'owapi'
urlpatterns = [
    # profile urls
    path('<token>/get/profile/', views.get_profile, name='get_profile'),
    path('<token>/get/dummy/', views.get_dummy, name='get_dummy'),
    path('<token>/get/rkhunter/', views.get_rkhunter, name='get_rkhunter'),
    path('<token>/get/rkhunter_app/', views.get_rkhunter_app, name='get_rkhunter_app'),
    path('<token>/get/yara/', views.get_yara, name='get_yara'),
    path('<token>/get/yara/rules/all/', views.get_yara_rules, name='get_yara_rules'),
    # submissions urls
    path('<token>/submit/yara/', views.submit_yara, name='submit_yara'),
    path('<token>/submit/rkhunter/', views.submit_rkhunter, name='submit_rkhunter'),
    path('<token>/submit/dummy/', views.submit_dummy, name='submit_dummy'),
]
