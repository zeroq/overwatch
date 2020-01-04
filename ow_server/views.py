# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from django.http import JsonResponse, StreamingHttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages

from ow_server.models import Server
from ow_server.forms import ServerForm

# Create your views here.

def index(request):
    context = {'servers': Server.objects.all()}
    return render(request, 'ow_server/list.html', context)

def edit_server(request):
    context = {}
    if request.method == 'POST':
        form = ServerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            sid = request.POST.get('server_id')
            server_obj, created = Server.objects.update_or_create(id=sid, defaults=cd)
            messages.info(request, 'Server modified!')
            return HttpResponseRedirect(reverse('owservers:index'))
        for item in form.errors.as_data():
            messages.error(request, 'Server data not valid! %s: %s' % (item, form.errors[item].as_text()))
        return HttpResponseRedirect(reverse('owservers:index'))
    else:
        s = Server.objects.all().first()
        if s != None:
            form = ServerForm(initial={'server_ip': s.server_ip, 'server_port': s.server_port})
            context['sid'] = s.id
        else:
            form = ServerForm()
            context['sid'] = 1
        context['form'] = form
        return render(request, 'ow_server/edit.html', context)
