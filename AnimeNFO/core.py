import urllib.request
import urllib.parse
import urllib.error
import urllib.parse
import requests
import re
import logging
from bs4 import BeautifulSoup

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
		string = ''.join(BeautifulSoup(result[0]).findAll(text=True))
		return BeautifulSoup(string)
	except IndexError:
		#logger.exception('Error finding result %s %s', regex, source)
		pass
	except Exception:
		#logger.exception('Error looking up %s in %s', regex, source)
		return default


def now_playing():
	# curl -d ajax=true -d mod=playing http://www.animenfo.com/radio/nowplaying.php
	page = requests.post(
		API_URL,
		data={'ajax': 'true', 'mod': 'playing'},
	)
	song = Song()
	soup = BeautifulSoup(page.text)
	if logger.isEnabledFor(logging.INFO):
		print(soup.prettify())
	#song.artist = soup.find(attrs={'data-search-artist': ''})
	song.title = soup.find(class_='icon-songinfo')['data-title']
	#song.album = soup.find(attrs={'data-search-album': ''})
	song.rating = _find('Rating: (.+?) .+<br/>', page.text, 'Rating')

	try:
		song.duration = soup.find(id='np_timer')['rel'], soup.find(id='np_time')['rel']
	except:
		song.duration = (0, 0)

	try:
		song.image = soup.find(id="nowplaying_albumart")['src']
	except:
		song.image = None

	if logger.isEnabledFor(logging.INFO):
		print(song)

	return song


def upcoming():
	# curl -d ajax=true -d mod=queue http://www.animenfo.com/radio/nowplaying.php
	page = requests.post(
		API_URL,
		data={'ajax': 'true', 'mod': 'queue', 'togglefull': 'true'},
	)
	results = BeautifulSoup(page.text).findAll('tr')

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
