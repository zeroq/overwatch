from django.contrib import admin

from ow_yara.models import YaraRule, YaraImport, YaraGroup

# Register your models here.

admin.site.register(YaraImport)
admin.site.register(YaraRule)
admin.site.register(YaraGroup)
