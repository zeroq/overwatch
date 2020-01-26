from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .forms import UploadFileForm
from .models import YaraRule, YaraImport, YaraGroup

import re

# Create your views here.

def index(request):
    rules = YaraRule.objects.all()
    return render(request, 'ow_yara/list.html', {'rules': rules})

def upload(request):
    """accept and process uploaded files
    """
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filename = request.FILES['file'].name
            ext = filename.rsplit('.',1)[1]
            if ext in ['yar', 'yara']:
                handle_uploaded_file(request, request.FILES['file'])
                messages.info(request, 'processing uploaded yara file')
            else:
                messages.error(request, 'wrong file extension, not processing')
            return HttpResponseRedirect(reverse('owyara:index'))
    else:
        form = UploadFileForm()
    return render(request, 'ow_yara/upload.html', {'form': form})

def handle_uploaded_file(request, f):
    """parse uploaded yara file for rule name and rule body and store it in the database
    """
    content = f.read().decode('utf-8')
    imp = re.compile('import\s\"(?P<import>.+?)\"', re.I|re.S)
    rule = re.compile('(private|\s)\srule\s(?P<rulename>.+?)\s*{(?P<rulebody>.+?condition:.+?)}',re.I|re.S)
    imports = imp.findall(content)
    rules = rule.findall(content)
    lst_imports = []
    for i in imports:
        iobj, created = YaraImport.objects.get_or_create(**{'name': i})
        lst_imports.append(iobj)
    for r in rules:
        robj, created = YaraRule.objects.get_or_create(**{'name': r[1], 'body': r[2]})
        for i in lst_imports:
            robj.imports.add(i)
        robj.save()
