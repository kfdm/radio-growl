import urllib, urllib2, re
from BeautifulSoup import BeautifulStoneSoup

BASE_URL = 'http://www.animenfo.com/radio/'
API_URL	= 'http://www.animenfo.com/radio/nowplaying.php'
PLAY_URL = 'http://www.animenfo.com/radio/listen.m3u'

#curl -d ajax=true -d mod=playing http://www.animenfo.com/radio/nowplaying.php

class Song(object):
	def __init__(self):
		self.artist = '<Artist>'
		self.title = '<Title>'
		self.album = '<Album>'
		self.duration = (0,0)
		self.rating = '<Rating>'
		self.image = '<Image>'
	def __str__(self):
		return '%s - %s - %s  [%s/%s]  Rating:[%s/10]'%(
			self.artist,
			self.title,
			self.album,
			self.duration[0],
			self.duration[1],
			self.rating
		)

def now_playing():
	data = urllib.urlencode({'ajax':'true','mod':'playing'})
	page = urllib2.urlopen(API_URL, data)
	page = page.read()
	song = Song()
	
	try: song.artist = re.findall('Artist: (.+?)<br/>', page)[0]
	except: song.artist = 'Artist'
	
	try: song.title = re.findall('Title: (.+?)<br/>', page)[0]
	except: song.title = 'Title'
	
	try: song.album = re.findall('Album: (.+?)<br/>', page)[0]
	except: song.album = 'Album'
	
	try: song.duration = re.findall('Duration: <span .+>(.+?)</span> / (.+?)<br/>', page)[0]
	except: song.duration = (0,0)
	
	try: song.rating = re.findall('Rating: (.+?) .+<br/>', page)[0]
	except: song.rating = 'Rating'
	
	try:
		song.image = re.findall('src="(pictures\/.+?)"',page)[0]
		song.image = BASE_URL+urllib.quote(song.image)
	except: song.image = None
	
	
	song.artist	= BeautifulStoneSoup(song.artist,convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
	song.title	= BeautifulStoneSoup(song.title,convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
	song.album	= BeautifulStoneSoup(song.album,convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
	
	return song

def upcomming():
	data = urllib.urlencode({'ajax':'true','mod':'queue','togglefull':'true'})
	page = urllib2.urlopen(API_URL, data)
	page = page.read()

	results = BeautifulStoneSoup(page).findAll('td')
	
	results.pop()
	
	songs = []
	for row in results:
		row = ''.join( row.findAll(text=True))
		if row.strip()==u'': continue
		row = BeautifulStoneSoup(row,convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
		row = row.__str__().strip()
		songs.append(row)
	return songs

if __name__=='__main__':
	song = now_playing()
	list = upcomming()
	print 'Now Playing'
	print song
	print song.image
	print
	print 'Upcomming'
	for item in list:
		print item
