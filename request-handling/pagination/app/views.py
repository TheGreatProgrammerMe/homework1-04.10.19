from django.shortcuts import render_to_response, redirect
from django.urls import reverse
import csv
from django.conf import settings
from django.core.paginator import Paginator
from urllib.parse import urlparse

def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    tN = []
    tS = []
    tD = []
    current_page = 1
    page_num = request.GET.get('page')
    if (page_num is not None):
    	current_page = int(page_num)
    countp = 10
    with open(settings.BUS_STATION_CSV, newline='') as csvfile:
	    reader = csv.DictReader(csvfile)
	    for row in reader:
	    	tN.append(row['Name'])
	    	tS.append(row['Street'])
	    	tD.append(row['District'])


    # не знаю, как по-другому
    paginator = Paginator(tN, countp)
    page = paginator.get_page(page_num)
    dataN = page.object_list
    dataNmsg = '<br>'.join(dataN)

    paginator = Paginator(tS, countp)
    page = paginator.get_page(page_num)
    dataS = page.object_list
    dataSmsg = '<br>'.join(dataS)

    paginator = Paginator(tD, countp)
    page = paginator.get_page(page_num)
    dataD = page.object_list
    dataDmsg = '<br>'.join(dataD)
    next_page_url = 'http://127.0.0.1:8000' + reverse('bus_stations') + '?page=' + str(current_page+1)

    return render_to_response('index.html', context={
        'bus_stations': [{'Name': dataNmsg, 'Street': dataSmsg, 'District': dataDmsg}],
        'current_page': current_page,
        'prev_page_url': None,
        'next_page_url': next_page_url,
    })
