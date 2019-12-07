# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from django.db import models
import django

# Create your models here.

class Profile(models.Model):
    profilename = models.CharField(max_length=1024, primary_key=True)   # e.g. "rkhunter"
    emergency_lockdown = models.BooleanField(default=False)             # e.g. disable network in case of finding

    def __str__(self):
        return "%s" % (self.profilename)

    def __unicode__(self):
        return u"%s" % (self.profilename)

class ScanItem(models.Model):
    scan = models.ForeignKey('Scan', on_delete=models.CASCADE)
    key = models.CharField(max_length=1024, db_index=True)
    value = models.CharField(max_length=2048, db_index=True)
    hit = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return "%s - %s - %s" % (self.key, self.value, self.hit)

    def __unicode__(self):
        return u"%s - %s - %s" % (self.key, self.value, self.hit)

class Scan(models.Model):
    scan_time = models.DateTimeField(db_index=True, default=django.utils.timezone.now)
    scan_type = models.CharField(max_length=1024, default='rkhunter', db_index=True)
    scan_result_raw = models.TextField()
    scan_client = models.ForeignKey('Client', on_delete=models.CASCADE)
    scan_status = models.CharField(max_length=20, default='processing', db_index=True)

    def __str__(self):
        return "%s (%s)" % (self.scan_type, self.scan_client.hostname)

    def __unicode__(self):
        return u"%s (%s)" % (self.scan_type, self.scan_client.hostname)

class Group(models.Model):
    groupname = models.CharField(max_length=1024, primary_key=True)
    description = models.TextField()
    groupprofile = models.ManyToManyField(Profile)

class Client(models.Model):
    hostname = models.CharField(max_length=1024, primary_key=True)
    ssh_ip = models.CharField(max_length=15, unique=True)
    ssh_keyfile_path = models.CharField(max_length=1024)
    ssh_user = models.CharField(max_length=128, db_index=True)
    ssh_pw = models.CharField(max_length=255, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=128)
    alive_time = models.DateTimeField(blank=True, null=True)
    profiles = models.ManyToManyField(Profile)
    groups = models.ManyToManyField(Group)
    debug = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % (self.hostname)

    def __unicode__(self):
        return u"%s" % (self.hostname)
