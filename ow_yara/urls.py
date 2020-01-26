# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from django.urls import include, path
from ow_yara import views


app_name = 'owyara'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
]
