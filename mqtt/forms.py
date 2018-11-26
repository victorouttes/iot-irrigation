from django import forms
from django.forms import ModelForm
from .models import ConfigMQTT


class ConfigMQTTForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = ConfigMQTT
        fields = ['host', 'port', 'username', 'password']

