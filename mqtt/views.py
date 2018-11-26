from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ConfigMQTTForm
from .models import ConfigMQTT
from .subscribe import main as mqtt


def edit(request):
    config = ConfigMQTT.objects.first()
    form = ConfigMQTTForm(request.POST or None, instance=config)
    if form.is_valid():
        c = form.save()
        mqtt(c)
        messages.success(request, 'Configuração salva com sucesso.')
        return redirect('config')
    data = {
        'form': form
    }
    return render(request, 'mqtt/edit.html', data)

