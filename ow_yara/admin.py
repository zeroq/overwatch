from django.contrib import admin

from ow_yara.models import YaraRule, YaraImport

# Register your models here.

admin.site.register(YaraImport)
admin.site.register(YaraRule)
