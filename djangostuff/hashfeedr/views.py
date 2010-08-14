# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from hashfeedr.forms import FilterForm
from django.http import HttpResponseRedirect
from urllib import quote

def landing_page(request):
	ctx = RequestContext(request)
	if request.method == 'POST':
		filterform = FilterForm(request.POST)
		if filterform.is_valid():
			return HttpResponseRedirect('/feed/' + quote(filterform.cleaned_data['query']))
		else:
			return render_to_response("landingpage.html",RequestContext(request, {'form': filterform}))
	else:
		filterform = FilterForm()
		return render_to_response("landingpage.html", RequestContext(request, {'form': filterform}))

def feeder(request, query):
	ctx = RequestContext(request)
	return render_to_response("feedr.html",ctx)
