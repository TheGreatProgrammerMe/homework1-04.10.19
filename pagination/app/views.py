from django.shortcuts import render_to_response, redirect
from django.urls import reverse
import csv
from django.conf import settings
from django.core.paginator import Paginator
from urllib.parse import urlparse

def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    objectreader = []
    current_page = 1
    page_num = request.GET.get('page')
    if (page_num is not None):
    	current_page = int(page_num)
    countp = 10
    with open(settings.BUS_STATION_CSV, newline='') as csvfile:
	    reader = csv.DictReader(csvfile)
	    for row in reader:
	    	objectreader.append([row['Name'],row['Street'],row['District']])

    paginator = Paginator(objectreader, countp)
    page = paginator.get_page(current_page)
    datalist = page.object_list
    dN = []
    dS = []
    dD = []
    for i in datalist:
    	dN.append(i[0])
    	dS.append(i[1])
    	dD.append(i[2])
    dN = '<br>'.join(dN)
    dS = '<br>'.join(dS)
    dD = '<br>'.join(dD)

    next_page_url = reverse('bus_stations') + '?page=' + str(current_page+1)

    return render_to_response('index.html', context={
        'bus_stations': [{'Name': dN, 'Street': dS, 'District': dD}],
        'current_page': current_page,
        'prev_page_url': None,
        'next_page_url': next_page_url,
    })
