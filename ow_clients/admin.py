# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from django.contrib import admin
from ow_clients.models import Client, Profile, Scan, ScanItem

# Register your models here.

admin.site.register(Client)
admin.site.register(Profile)
admin.site.register(Scan)
admin.site.register(ScanItem)
