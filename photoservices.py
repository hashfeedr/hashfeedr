#some functions for converting tweeted urls from picture hosting services to direct links to the jpeg
import re
from urllib import quote

def getThumbFromURL(url):
	if re.match(r"^http://yfrog\.(com|ru|it|fr|co.il|co.uk|com.pl|pl|eu)/(\d|\w)+(j|p|b|g|t)$", url) is not None:
		return yFrog(url)
	elif re.match(r"^http://twitpic\.com", url) is not None:
		return twitPic(url)
	elif re.match(r"^http://moby.to/(\d|\w)+(j|p|b|g|t)$", url) is not None:
		return mobyPicture(url)
	elif re.match(r"^http://tweetphoto\.com/\d+$", url):
		return tweetPhoto(url)
	else:
		return False

def yFrog(url):
	return url + '.th.jpg'

def twitPic(url):
	matches = re.search(r"^http://twitpic\.com/((\d|\w)+)", url)
	if(matches is not None):
		return 'http://twitpic.com/show/thumb/' + matches.group(1)
	else:
		return False
		
def mobyPicture(url):
	return url + ':thumb'
	
def tweetPhoto(url):
	return "http://TweetPhotoAPI.com/api/TPAPI.svc/imagefromurl?size=thumb&url=" + quote(url)