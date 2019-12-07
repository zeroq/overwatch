# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from django.core.management.base import BaseCommand, CommandError

from ow_clients.models import Client, Scan, ScanItem

import json
import pprint

class Command(BaseCommand):
    def handle(self, *args, **options):
        scans = Scan.objects.filter(scan_status='processing')
        for scan in scans:
            found = False
            try:
                jrsp = json.loads(scan.scan_result_raw)
            except Exception as e:
                print(e)
                continue
            print(jrsp.keys())
            if 'check of known rootkit files and directories' in jrsp:
                for rk in jrsp['check of known rootkit files and directories']:
                    value = jrsp['check of known rootkit files and directories'][rk]
                    if value != 'Not found':
                        result = True
                        found = True
                    else:
                        result = False
                    scan_item = {
                        'scan': scan,
                        'key': rk,
                        'value': value,
                        'hit': result
                    }
                    item, created = ScanItem.objects.get_or_create(**scan_item)
            if 'group and account checks' in jrsp:
                for rk in jrsp['group and account checks']:
                    value = jrsp['group and account checks'][rk]
                    print(rk, value)
            scan.scan_status = 'finished'
            if found:
                scan.scan_client.last_status = 'Issues Detected'
            else:
                scan.scan_client.last_status = 'Clean'
            scan.scan_client.save()
            scan.save()
