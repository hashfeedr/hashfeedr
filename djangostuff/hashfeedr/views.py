# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext

def landing_page(request):
	ctx = RequestContext(request)
	return render_to_response("landingpage.html",ctx)

def feeder(request, query):
	ctx = RequestContext(request)
	return render_to_response("feedr.html",ctx)
