import urllib,urllib2,re,os,htmlentitydefs
import xbmcplugin,xbmcgui,xbmcaddon
from BeautifulSoup import BeautifulStoneSoup

__settings__ = xbmcaddon.Addon(id='plugin.video.5by5')
__language__ = __settings__.getLocalizedString
home = __settings__.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )

# options
option_label = __settings__.getSetting( "label" )
option_banner = __settings__.getSetting( "banner" )

def converthtml(text):
		def fixup(m):
				text = m.group(0)
				if text[:2] == "&#":
						# character reference
						try:
								if text[:3] == "&#x":
										return unichr(int(text[3:-1], 16))
								else:
										return unichr(int(text[2:-1]))
						except ValueError:
								pass
				else:
						# named entity
						try:
								text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
						except KeyError:
								pass
				return text # leave as is
		return re.sub("&#?\w+;", fixup, text)

def getShows():
		url='http://5by5.tv/rss-boxee'
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		soup = BeautifulStoneSoup(link)
		shows = soup('item')
		for show in shows:
				name = show.title.string
				url = show.link.string
				url = url.replace('rss://', 'http://')
				description = show.description.string
				aired = show.pubdate.string
				year = aired[12:16]
				day = aired[5:7]
				month = aired[8:11]
				if month == 'Jan':
						month = '01'
				elif month == 'Feb':
						month = '02'
				elif month == 'Mar':
						month = '03'
				elif month == 'Apr':
						month = '04'
				elif month == 'May':
						month = '05'
				elif month == 'Jun':
						month = '06'
				elif month == 'Jul':
						month = '07'
				elif month == 'Aug':
						month = '08'
				elif month == 'Sep':
						month = '09'
				elif month == 'Oct':
						month = '10'
				elif month == 'Nov':
						month = '11'
				elif month == 'Dec':
						month = '12'
				aired = year+'-'+month+'-'+day
				img = show('boxee:image')[0]
				img = ' '.join(img)
				img = img.replace('<boxee:image>', '')
				img = img.replace('-big.jpg', '-large.jpg')
				if option_banner == "true":
						img = img.replace('/cover_art/', '/images/')
				addDir(name,url,description,aired,1,img)
	

def index(url):
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		soup = BeautifulStoneSoup(link)
		eps = soup('item')
		eps.reverse()
		for ep in eps:
				name = ep.title.string
				name = unicode(name).encode("utf-8")
				name = converthtml(name)
				url = ep.link.string
				description = ep.description.string
				description = unicode(description).encode("utf-8")
				description = converthtml(description)
				img = ep('boxee:image')[0]
				img = ' '.join(img)
				img = img.replace('<boxee:image>', '')
				img = img.replace('-big.jpg', '-large.jpg')
				if option_banner == "true":
						img = img.replace('/cover_art/', '/images/')
				cast = ep('boxee:cast')[0]
				cast = ' '.join(cast)
				cast = cast.replace('<boxee:cast>', '')
				cast = unicode(cast).encode("utf-8")
				cast = converthtml(cast)
				aired = ep.pubdate.string
				year = aired[12:16]
				day = aired[5:7]
				month = aired[8:11]
				if month == 'Jan':
								month = '01'
				elif month == 'Feb':
								month = '02'
				elif month == 'Mar':
								month = '03'
				elif month == 'Apr':
								month = '04'
				elif month == 'May':
								month = '05'
				elif month == 'Jun':
								month = '06'
				elif month == 'Jul':
								month = '07'
				elif month == 'Aug':
								month = '08'
				elif month == 'Sep':
								month = '09'
				elif month == 'Oct':
								month = '10'
				elif month == 'Nov':
								month = '11'
				elif month == 'Dec':
								month = '12'
				aired = year+'-'+month+'-'+day
				# Unrelated Video Override
				if name == "#9: 7 Inches":
						url = "http://audio.5by5.tv/broadcasts/talkshow/2010/talkshow-009.mp3"
				if url.find('.mp4') != -1:
								label = 'Video'
								if (option_label == "3" or option_label == "2"):
												name = name+" (Video)"
								addLink(name,url,description,1,img,label,cast,aired,"video")
				elif url.find('.mp3') != -1:
								label = 'Audio'
								if (option_label == "3" or option_label == "1"):
												name = name+" (Audio)"
								addLink(name,url,description,1,img,label,cast,aired,"audio")


def get_params():
		param=[]
		paramstring=sys.argv[2]
		if len(paramstring)>=2:
				params=sys.argv[2]
				cleanedparams=params.replace('?','')
				if (params[len(params)-1]=='/'):
						params=params[0:len(params)-2]
				pairsofparams=cleanedparams.split('&')
				param={}
				for i in range(len(pairsofparams)):
						splitparams={}
						splitparams=pairsofparams[i].split('=')
						if (len(splitparams))==2:
								param[splitparams[0]]=splitparams[1]
								
		return param


def addLink(name,url,description,length,iconimage,label,cast,aired,medium):
		ok=True
		liz=xbmcgui.ListItem(name, label, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
		if medium == "video":
				liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description, "Duration": length, "Cast": cast, "Aired": aired } )
		elif medium == "audio":
				liz.setInfo( type="Music", infoLabels={ "Title": name, "Lyrics": description, "Artist": cast, "Date": aired } )
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
		return ok


def addDir(name,url,description,aired,mode,iconimage):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description, "Aired": aired } )
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
		return ok
		
			
params=get_params()
url=None
name=None
mode=None

try:
		url=urllib.unquote_plus(params["url"])
except:
		pass
try:
		name=urllib.unquote_plus(params["name"])
except:
		pass
try:
		mode=int(params["mode"])
except:
		pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None:
		print ""
		getShows()
	
elif mode==1:
		print ""+url
		index(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
