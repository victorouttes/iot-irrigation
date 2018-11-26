from django.db import models
from django import forms


class ConfigMQTT(models.Model):
    host = models.CharField(blank=False, null=False, max_length=255)
    port = models.CharField(blank=False, null=False, max_length=8)
    username = models.CharField(blank=False, null=False, max_length=30)
    password = models.CharField(blank=False, null=False, max_length=30)
