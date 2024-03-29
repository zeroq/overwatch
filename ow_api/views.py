# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import os
import paramiko
import datetime
import json
import base64

from django.http import JsonResponse, StreamingHttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from ow_clients.models import Client, Scan, ScanItem
from ow_yara.models import YaraRule, YaraGroup, YaraImport
from ow_yara.utils import compile_all_rules

# Token decorator
def is_allowed(func):
    """ decorator to check token
    """
    def decorator(request, token):
        resp = {'msg': 'Not allowed!'}
        try:
            cl = Client.objects.get(token=token)
            return func(request, token)
        except Client.DoesNotExist:
            return JsonResponse(resp)
        return JsonResponse(resp)
    return decorator

#########################
# Get profile Endpoints #
#########################

@is_allowed
def get_dummy(request, token):
    """ dummy profile
    """
    resp = {'msg': 'Successfully connected', 'cmd': 'Dummy', 'data': ''}
    return JsonResponse(resp)

@is_allowed
def get_profile(request, token):
    """get the current active profile for host
    """
    cl = Client.objects.get(token=token)
    # update alive time
    cl.alive_time = datetime.datetime.now(datetime.timezone.utc)
    cl.save()
    # profile list
    pr = []
    for profile in cl.profiles.all():
        pr.append(profile.profilename)
    resp = {'msg': 'Successfully connected', 'profiles': pr}
    return JsonResponse(resp)

@is_allowed
def get_rkhunter(request, token):
    """ get rkhunter execution and parsing app
    """
    # get hunter python script
    rkhunter_file = os.path.join(settings.BASE_DIR, 'ow_downloads', 'rkhunter_parse.py')
    with open(rkhunter_file, 'rb') as fp:
        content = base64.b64encode(fp.read())
    # TODO: create scan job
    resp = {'msg': 'Successfully connected', 'cmd': 'run', 'data': content.decode('utf8')}
    return JsonResponse(resp)

@is_allowed
def get_rkhunter_app(request, token):
    """ get recent rkhunter software directly from server
    """
    # get hunter install file
    rkhunter_file = os.path.join(settings.BASE_DIR, 'ow_downloads', 'rkhunter-1.4.6.tar.gz')
    with open(rkhunter_file, 'rb') as fp:
        content = base64.b64encode(fp.read())
    # TODO: create job
    resp = {'msg': 'Successfully connected', 'cmd': 'install', 'data': content.decode('utf8')}
    return JsonResponse(resp)

@is_allowed
def get_yara(request, token):
    """ get yara execution script
    """
    # get yara huter python script
    yhunter_file = os.path.join(settings.BASE_DIR, 'ow_downloads', 'ow_yara_hunter.py')
    with open(yhunter_file, 'rb') as fp:
        content = base64.b64encode(fp.read())
    # TODO: create yara job
    resp = {'msg': 'Successfully connected', 'cmd': 'run', 'data': content.decode('utf8')}
    return JsonResponse(resp)

@is_allowed
def get_yara_rules(request, token):
    """ download all rules
    """
    res, error  = compile_all_rules()
    if res != None:
        temp_file = os.path.join(settings.FILE_TEMP_PATH, 'all_yara.yar')
        with open(temp_file, 'rb') as fp:
            content = base64.b64encode(fp.read())
        resp = {'msg': 'Successfully connected', 'cmd': 'rules', 'data': content.decode('utf8')}
        return JsonResponse(resp)
    resp = {'msg': 'Failed creating yara rules', 'cmd': 'error', 'data': None}
    return JsonResponse(resp)


@is_allowed
def get_systeminfo(request, token):
    """ gather system information
    """
    # get systeminfo script
    systeminfo_file = os.path.join(settings.BASE_DIR, 'ow_downloads', 'ow_systeminformation.py')
    with open(systeminfo_file, 'rb') as fp:
        content = base64.b64encode(fp.read())
    # TODO: create info job
    resp = {'msg': 'Successfully connected', 'cmd': 'run', 'data': content.decode('utf8')}
    return JsonResponse(resp)

########################
# Submission Functions #
########################

@csrf_exempt
@is_allowed
def submit_dummy(request, token):
    cl = Client.objects.get(token=token)
    if request.method == 'POST':
        submission_time = datetime.datetime.now(datetime.timezone.utc)
        return JsonResponse({'msg': 'successfull submitted'})
    else:
        return JsonResponse({'msg': 'wrong method'})

@csrf_exempt
@is_allowed
def submit_rkhunter(request, token):
    """ receive result data from last rkhunter scan
    """
    cl = Client.objects.get(token=token)
    if request.method == 'POST':
        if 'profile' in request.POST and 'data' in request.POST and 'errors' in request.POST:
            try:
                rkjson = json.loads(request.POST['data'])
                submission_time = datetime.datetime.now(datetime.timezone.utc)
                scan = {
                    'scan_time': submission_time,
                    'scan_type': 'rkhunter',
                    'scan_result_raw': json.dumps(rkjson),
                    'scan_client': cl,
                    'scan_status': 'processing'
                }
                sobj = Scan(**scan)
                sobj.save()
                return JsonResponse({'msg': 'successfull submitted'})
            except Exception as e:
                print(e)
                print("Failed loading rkhunter json response")
                return JsonResponse({'msg': 'wrong or missing data submitted'})
        else:
            print(request.POST)
            return JsonResponse({'msg': 'wrong or missing data submitted'})
    else:
        return JsonResponse({'msg': 'wrong method'})

@csrf_exempt
@is_allowed
def submit_yara(request, token):
    """receive result data from yara scan
    """
    cl = Client.objects.get(token=token)
    if request.method == 'POST':
        # TODO: get and process results
        pass
    else:
        return JsonResponse({'msg': 'wrong method'})

# GUI API Functions


