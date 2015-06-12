import urllib.request
import urllib.parse
import urllib.error
import urllib.parse
import re
import logging
from bs4 import BeautifulStoneSoup

logger = logging.getLogger(__name__)

__all__ = [
	'API_URL',
	'PLAY_URL',
	'Song',
	'now_playing',
	'upcoming',
]

BASE_URL = 'https://www.animenfo.com/radio/'
API_URL = 'https://www.animenfo.com/radio/nowplaying.php'
PLAY_URL = 'https://www.animenfo.com/radio/listen.m3u'


class Song(object):
	def __init__(self):
		self.artist = '<Artist>'
		self.title = '<Title>'
		self.album = '<Album>'
		self.duration = (0, 0)
		self.rating = '<Rating>'
		self.image = '<Image>'

	def __str__(self):
		return '%s - %s - %s  [%s/%s]  Rating:[%s/10]' % (
			self.artist,
			self.title,
			self.album,
			self.duration[0],
			self.duration[1],
			self.rating
		)


def _find(regex, source, default):
	'''Find a string using a regex and strip extra HTML'''
	try:
		result = re.findall(regex, source)
		print(result)
		string = ''.join(BeautifulStoneSoup(result[0]).findAll(text=True))
		return BeautifulStoneSoup(string, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
	except:
		logger.exception('Error looking up %s', regex)
		return default


def now_playing():
	# curl -d ajax=true -d mod=playing http://www.animenfo.com/radio/nowplaying.php
	data = urllib.parse.urlencode({'ajax': 'true', 'mod': 'playing'})
	page = urllib.request.urlopen(API_URL, data)
	page = page.read()
	song = Song()

	song.artist = _find('<span data-search-artist >(.+?)</span>', page, 'Artist')
	song.title = _find('Title:</span> (.+?)<br/>', page, 'Title')
	song.album = _find('<span data-search-album >(.+?)</span>', page, 'Album')
	song.rating = _find('Rating: (.+?) .+<br/>', page, 'Rating')

	try:
		song.duration = re.findall('Duration: <span .+>(.+?)</span> / <span .+>(.+?)</span><br/>', page)[0]
	except:
		song.duration = (0, 0)

	try:
		song.image = re.findall('src="(radio\/albumart\/.+?)"', page)[0]
		print(song.image)
		song.image = BASE_URL + urllib.parse.quote(song.image)
	except:
		song.image = None

	return song


def upcoming():
	# curl -d ajax=true -d mod=queue http://www.animenfo.com/radio/nowplaying.php
	data = urllib.parse.urlencode({'ajax': 'true', 'mod': 'queue', 'togglefull': 'true'})
	page = urllib.request.urlopen(API_URL, data)
	page = page.read()

	results = BeautifulStoneSoup(page).findAll('tr')

	results.pop()

	songs = []
	for row in results:
		row = ''.join(row.findAll(text=True))
		if row.strip() == '':
			continue
		row = BeautifulStoneSoup(row, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
		row = row.__str__().strip()
		row = re.sub('\s+', ' ', row)
		songs.append(row)
	return songs


def main():
	song = now_playing()
	list = upcoming()
	print('Now Playing')
	print(song)
	if song.image:
		print(song.image.replace(' ', '%20'))
	print()
	print('Upcoming')
	for item in list:
		print(item)


def simple():
	print(now_playing())

if __name__ == '__main__':
	main()
