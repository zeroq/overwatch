# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from overwatch.serializers import UserSerializer, GroupSerializer, ClientSerializer
from ow_clients.models import Client, Scan

import paramiko
from io import StringIO

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

def home(request):
    context = {'scans': Scan.objects.all().order_by('scan_time')[:15]}
    return render(request, 'overwatch/index.html', context)
