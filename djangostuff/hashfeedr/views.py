# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from urllib import quote

def landing_page(request):
		return render_to_response("landingpage.html", RequestContext(request))

def feeder(request, query):
	ctx = RequestContext(request)
	return render_to_response("feedr.html",ctx)

def gofeed(request):
	return HttpResponseRedirect('/feed/' + quote(request.GET['query']))