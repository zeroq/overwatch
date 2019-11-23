# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from django.db import models

# Create your models here.

class Server(models.Model):
    server_ip = models.CharField(max_length=15, unique=True)
    server_port = models.IntegerField(default=8000)
