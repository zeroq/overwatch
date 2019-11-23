# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from django.contrib.auth.models import User, Group
from rest_framework import serializers

from ow_clients.models import Client

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ['hostname', 'ssh_ip', 'ssh_user', 'ssh_keyfile_path', 'ssh_pw', 'token']
