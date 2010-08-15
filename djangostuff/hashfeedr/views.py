# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from urllib import quote
import tweetpreloader

def landing_page(request):
		return render_to_response("landingpage.html", RequestContext(request))

def feeder(request, query):
	initials = tweetpreloader.getInitialTweets(query)
	return render_to_response("feedr.html", RequestContext(request, {'initialtweets': initials}))

def gofeed(request):
	return HttpResponseRedirect('/feed/' + quote(request.GET['query']))