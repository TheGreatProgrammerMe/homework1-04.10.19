from django.shortcuts import render_to_response, redirect
from django.urls import reverse
import csv
from django.conf import settings
from django.core.paginator import Paginator
from urllib.parse import urlparse

def index(request):
	return redirect(reverse(bus_stations))

def bus_stations(request):
	current_page = 1
	objectreader = []
	page_num = request.GET.get('page')

	if (page_num is not None):
		current_page = int(page_num)

	with open(settings.BUS_STATION_CSV, newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			tlist = (
				{'Name' : row['Name'], 
				'Street' : row['Street'], 
				'District' : row['District']})
			objectreader.append(tlist)

	paginator = Paginator(objectreader, 10)
	page = paginator.get_page(current_page)
	datalist = page.object_list
	
	if page.has_next():
		next_page_url = reverse('bus_stations') + '?page=' + str(page.next_page_number())
		if (page_num is not None): current_page = page.next_page_number()-1
	else:
		next_page_url = None
		
	if page.has_previous():
		previous_page_url = reverse('bus_stations') + '?page=' + str(page.previous_page_number())
		if (page_num is not None): current_page = page.previous_page_number()+1
	else:
		previous_page_url = None

	return render_to_response('index.html', context={
		'bus_stations': datalist,
		'current_page': current_page,
		'prev_page_url': previous_page_url,
		'next_page_url': next_page_url,
	})
