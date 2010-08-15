# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from urllib import quote
import tweetpreloader
from tophashfeeds import getMostPopularHashes
import settings
import json

def landing_page(request):
	toptweets = map(lambda keyw: (keyw[0], quote(keyw[0]), keyw[1]), getMostPopularHashes(10)) 
	
	return render_to_response("landingpage.html", RequestContext(request, {'toptweets': toptweets}))

def feeder(request, query, ignoreme):
	initials = tweetpreloader.getInitialTweets(query)
	js_safe_query = json.dumps(query).strip('""');
	return render_to_response("feedr.html", RequestContext(request, {'initialtweets': initials, 'keyword': js_safe_query, 'websocket_url': settings.WEBSOCKET_URL + quote(query)}))

def gofeed(request):
	return HttpResponseRedirect('/feed/' + quote(request.GET['query']))