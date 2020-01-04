
from django.forms import ModelForm

from ow_server.models import Server

class ServerForm(ModelForm):
    class Meta:
        model = Server
        fields = ['server_ip', 'server_port']

    def __init__(self, *args, **kwargs):
        super(ServerForm, self).__init__(*args, **kwargs)
        self.fields['server_ip'].widget.attrs.update({'class' : 'form-control', 'id': 'server_ip'})
        self.fields['server_port'].widget.attrs.update({'class' : 'form-control', 'id': 'server_port'})
