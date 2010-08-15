# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from urllib import quote
import tweetpreloader
from tophashfeeds import getMostPopularHashes
import settings

def landing_page(request):
	toptweets = map(lambda keyw: (keyw, quote(keyw)), getMostPopularHashes(5)) 
	
	return render_to_response("landingpage.html", RequestContext(request, {'toptweets': toptweets}))

def feeder(request, query, ignoreme):
	initials = tweetpreloader.getInitialTweets(query)
	return render_to_response("feedr.html", RequestContext(request, {'initialtweets': initials, 'keyword': query, 'websocket_url': settings.WEBSOCKET_URL + query}))

def gofeed(request):
	return HttpResponseRedirect('/feed/' + quote(request.GET['query']))