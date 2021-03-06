# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from django.http import JsonResponse, StreamingHttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.contrib import messages

from ow_clients.models import Client, Scan
from ow_clients.forms import ClientForm, EditClientForm
from ow_server.models import Server

import os
import paramiko
import io
import re
import hashlib
import time

# Create your views here.

def index(request):
    context = {'clients': Client.objects.all()}
    return render(request, 'ow_clients/list.html', context)

def edit_client(request, hostname):
    """ edit an existing client item
    """
    try:
        cl = Client.objects.get(hostname=hostname)
    except Exception as e:
        messages.error(request, 'Client data not valid! %s' % (e))
        return HttpResponseRedirect(reverse('owclients:index'))
    context = {}
    if request.method == 'POST':
        form = EditClientForm(request.POST, instance=cl)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('owclients:index'))
        for item in form.errors.as_data():
            messages.error(request, 'Client data not valid! %s: %s' % (item, form.errors[item].as_text()))
        return HttpResponseRedirect(reverse('owclients:index'))
    else:
        form = EditClientForm(instance=cl)
        context['form'] = form
        return render(request, 'ow_clients/edit.html', context)

def create_client(request):
    """ create a new client item
    """
    context = {}
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            token = hashlib.sha256(str(time.time()).encode('utf8')).hexdigest()
            obj = form.save(commit=False)
            obj.token = token
            obj.save()
            messages.info(request, 'New client created!')
            return HttpResponseRedirect(reverse('owclients:index'))
        for item in form.errors.as_data():
            messages.error(request, 'Client data not valid! %s: %s' % (item, form.errors[item].as_text()))
        return HttpResponseRedirect(reverse('owclients:index'))
    else:
        form = ClientForm()
        context['form'] = form
        return render(request, 'ow_clients/create.html', context)

def delete_client(request, hostname):
    """ delete client
    """
    try:
        cl = Client.objects.get(hostname=hostname)
        cl.delete()
    except Exception as e:
        messages.error(request, 'Client data not valid! %s' % (e))
        return HttpResponseRedirect(reverse('owclients:index'))
    return HttpResponseRedirect(reverse('owclients:index'))

def view_scan_results(request, hostname, scanid):
    """ show scan results
    """
    context = {}
    try:
        cl = Client.objects.get(hostname=hostname)
    except Exception as e:
        messages.error(request, 'Client data not valid! %s' % (e))
        return HttpResponseRedirect(reverse('owclients:index'))
    context['client'] = cl
    try:
        sc = Scan.objects.get(id=scanid)
    except Exception as e:
        messages.error(request, 'Scan data not valid! %s' % (e))
        return HttpResponseRedirect(reverse('owclients:index'))
    context['scan'] = sc
    context['scan_results'] = sc.scanitem_set.all()
    context['scan_hits'] = sc.scanitem_set.filter(hit=True).count()
    return render(request, 'ow_clients/scan_results.html', context)

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
        msg = 'transfer complete'
        messages.success(request, msg)
    except Exception as e:
        print(e)
        msg = 'Failed to connect (%s)!' % (e)
        messages.error(request, msg)
    return HttpResponseRedirect(reverse('owclients:index'))

