# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, redirect
from django.urls import reverse
from django.contrib import auth
from django.template.context_processors import csrf
from django.utils.encoding import smart_str
from collections import Counter
import operator, json, datetime

ids = []
d = json.load(open('pizza/static/pizza/points.json', encoding="utf8"))
for i in range(0, len(d)):
	ids.append(i)

def index(request):
	out = []
	if not -1 in ids:
		for i in ids:
			out.append(i)
		return render(request, 'index.html', {"ids":out})
	else:
		return render(request, 'index.html', {"ids":[]})
def attr(request):
	ids.clear()
	ides = []
	if request.POST:
		box = request.POST.getlist("company")
		time_str = request.POST.get("time")
		metro = request.POST.getlist("metro")
		if len(time_str):
			print("more")
			for i in range(0, len(d)):
				if d[i]["company"] in box:
					time = time_str.split(':')
					time[0] = (int)(time[0])
					time[1] = (int)(time[1])
					time_s = d[i]["time_s"].split(':')
					time_e = d[i]["time_e"].split(':')
					time_s[0] = (int)(time_s[0])
					time_e[0] = (int)(time_e[0])
					time_s[1] = (int)(time_s[1])
					time_e[1] = (int)(time_e[1])
					if time_e[0] <= 6:
						time_e[0] += 24
					result1 = True
					result2 = True

					if time_s[0] > time[0]:
						result1 = False
					elif time_s[0] == time[0] and time_s[1] > time[1]:
						result1 = False
					elif time_e[0] < time[0]:
						result1 = False
					elif time_e[0] == time[0] and time_e[1] < time[1]:
						result1 = False

					time[0] += 24

					if time_s[0] > time[0]:
						result2 = False
					elif time_s[0] == time[0] and time_s[1] > time[1]:
						result2 = False
					elif time_e[0] < time[0]:
						result2 = False
					elif time_e[0] == time[0] and time_e[1] < time[1]:
						result2 = False

					if result1 or result2:
						ides.append(i)
			if len(ides) == 0:
				ids.append(-1)
				return redirect('/')
		else:
			if len(box) > 0:
				for i in range(0, len(d)):
					if d[i]["company"] in box:
						ides.append(i)
			else:
				for i in range(0, len(d)):
					ides.append(i)
		if len(metro) > 0:
			for i in ides:
				l = list((Counter(metro)&Counter(d[i]["metro"])).elements())
				if len(l) > 0:
					ids.append(i)
		else:
			for i in range(0, len(d)):
				ids.append(i)
	return redirect('/')