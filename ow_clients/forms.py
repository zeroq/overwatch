
from django.forms import ModelForm

from ow_clients.models import Client

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['hostname', 'ssh_ip', 'ssh_keyfile_path', 'ssh_user', 'ssh_pw']

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['hostname'].widget.attrs.update({'class' : 'form-control', 'id': 'hostname'})
        self.fields['ssh_ip'].widget.attrs.update({'class' : 'form-control', 'id': 'ssh_ip'})
        self.fields['ssh_keyfile_path'].widget.attrs.update({'class' : 'form-control', 'id': 'ssh_keyfile_path'})
        self.fields['ssh_user'].widget.attrs.update({'class' : 'form-control', 'id': 'ssh_user'})
        self.fields['ssh_pw'].widget.attrs.update({'class' : 'form-control', 'id': 'ssh_pw'})
