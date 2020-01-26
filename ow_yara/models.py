from django.db import models

# Create your models here.


class YaraImport(models.Model):
    name = models.CharField(max_length=2048, primary_key=True)

class YaraRule(models.Model):
    name = models.CharField(max_length=2048, primary_key=True)  # rule name should be unique
    imports = models.ManyToManyField(YaraImport, blank=True)
    body = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=True)

class YaraGroup(models.Model):
    name = models.CharField(max_length=2048, primary_key=True)
    rules = models.ManyToManyField(YaraRule, blank=True)
