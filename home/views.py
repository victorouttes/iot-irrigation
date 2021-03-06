from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage
import json
from .models import Sensor, IrrigationStatus
from mqtt.mqtt import publish


ITEMS_PER_PAGE = 10


@login_required
def home(request):
    button = 'OFF'
    if IrrigationStatus.objects.all().exists():
        status = IrrigationStatus.objects.latest('id')
        button = status.status

    if Sensor.objects.all().exists():
        sensor = Sensor.objects.latest('id')
        count = Sensor.objects.all().count()
        data = {'sensor': sensor, 'count': count, 'status': button}
    else:
        data = {'sensor': None, 'count': 0, 'status': button}
    return render(request, 'home/home.html', data)


@login_required
def list_all(request):
    page = request.GET.get('page')
    paginator = Paginator(Sensor.objects.order_by('-date').all(), ITEMS_PER_PAGE)
    total = paginator.count

    try:
        alldata = paginator.page(page)
    except InvalidPage:
        alldata = paginator.page(1)

    data = {'alldata': alldata, 'total': total}
    return render(request, 'home/data.html', data)


@login_required
def chart(request):
    alldata = Sensor.objects.order_by('-date')[:3000][::-1]
    dates = [x.date.strftime('%d/%m/%Y %H:%M:%S') for x in alldata]
    humidities = [float(x.humidity) for x in alldata]
    temperatures = [float(x.temperature) for x in alldata]
    sunlights = [float(x.sunlight) for x in alldata]
    data = {
        'dates': json.dumps(dates),
        'humidities': json.dumps(humidities),
        'temperatures': json.dumps(temperatures),
        'sunlights': json.dumps(sunlights)
    }
    return render(request, 'home/chart.html', data)


@login_required
def irrigation(request):
    if request.method == 'POST':
        novo = IrrigationStatus()
        novo.status = 'ON'
        if IrrigationStatus.objects.all().exists():
            status = IrrigationStatus.objects.latest('id')
            if status.status == 'ON':
                novo.status = 'OFF'
        novo.save()
        publish(novo.status)
    return home(request)
