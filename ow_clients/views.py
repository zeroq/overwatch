# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.conf import settings

from ow_clients.models import Client
from ow_server.models import Server

import os
import paramiko
import io
import re

# Create your views here.

def index(request):
    context = {'clients': Client.objects.all()}
    return render(request, 'ow_clients/list.html', context)

def get_rkhunter(request, hostname):
    """ get recent rkhunter software directly from server
    """
    rkhunter_file = os.path.join(settings.BASE_DIR, 'ow_downloads', 'rkhunter-1.4.6.tar.gz')
    fp = open(rkhunter_file, 'rb')
    content = fp.read()
    fp.close()
    resp = StreamingHttpResponse(streaming_content=content)
    return resp

def deploy(request, hostname):
    resp = {'msg': None}
    cl = Client.objects.get(hostname=hostname)
    deploy_file = 'ow_agent.py'
    localpath = os.path.join(settings.BASE_DIR, 'ow_downloads', deploy_file)
    # read agent file and replace settings
    ow_server = Server.objects.first()
    fp = open(localpath, 'r')
    agent = fp.read()
    fp.close()
    agent = agent.replace('<OW_TOKEN>', str(cl.token))
    agent = agent.replace('<OW_IP>', str(ow_server.server_ip))
    agent = agent.replace('<OW_PORT>', str(ow_server.server_port))
    if cl.debug:
        agent = agent.replace('logging.INFO', 'logging.DEBUG')
    # deploy remote
    remotepath = deploy_file
    try:
        ssh = paramiko.SSHClient()
        key = paramiko.RSAKey.from_private_key_file(cl.ssh_keyfile_path)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(cl.ssh_ip, username=cl.ssh_user, pkey=key, timeout=10)
        sftp = ssh.open_sftp()
        # transfer agent script
        sftp.putfo(io.BytesIO(str.encode(agent)), remotepath)
        sftp.close()
        # execute agent script
        command = 'python3 %s' % remotepath
        ssh.exec_command(command)
        ssh.close()
        resp['msg'] = 'transfer complete'
    except Exception as e:
        print(e)
        resp['msg'] = 'Failed to connect (%s)!' % (e)
    return JsonResponse(resp)
