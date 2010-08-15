function initFromSearchAPI(keyword) {
	$.getJSON("http://search.twitter.com/search.json?callback=?", { 'q': keyword, 'rpp': 5}, function(data) {
		for(var j in data) {
			var inv = data[j];
				for(var i in inv) {
					tweets[tweets.length]=([new Tweet(inv[i].text,inv[i].profile_image_url,inv[i].from_user)]);
					var t=tweets[tweets.length-1];
					new Transition(cam.position,cam.position.value,[t[0].position.value[0]+t[0].width*0.5,t[0].position.value[1]+t[0].height*0.5,calcangle()],20.0);
				}
			}	
	});
	
}