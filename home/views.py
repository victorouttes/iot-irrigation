from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage
from .models import Sensor


ITEMS_PER_PAGE = 10


@login_required
def home(request):
    sensor = Sensor.objects.latest('id')
    count = Sensor.objects.all().count()
    data = {'sensor': sensor, 'count': count}
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
