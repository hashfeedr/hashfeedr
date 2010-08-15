# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from urllib import quote
import tweetpreloader
from redisstats import RedisStats
import settings
import json
import re

def landing_page(request):
	stats = RedisStats()
	toptweets = map(lambda keyw: (keyw[0], quote(keyw[0]), keyw[1]), stats.getMostPopularHashes(10)) 
	tpm = stats.getTweetsPerMinute()
	streams = stats.getStreamCnt()
	return render_to_response("landingpage.html", RequestContext(request, {'toptweets': toptweets, 'streams': streams, 'tpm': tpm}))

def feeder(request, query, ignoreme):
	initials = tweetpreloader.getInitialTweets(query)
	js_safe_query = json.dumps(query).strip('""');
	keywords = set(re.split(r"[,\s]\s*", query));
	return render_to_response("feedr.html", RequestContext(request, {'initialtweets': initials, 'keyword': js_safe_query, 'keywords': keywords, 'websocket_url': settings.WEBSOCKET_URL + quote(query)}))

def gofeed(request):
	return HttpResponseRedirect('/feed/' + quote(request.GET['query']))