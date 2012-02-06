import logging
logger = logging.getLogger(__name__)
import urllib2
from clint import resources

resources.init('kfdm', 'radio-growl')


def image_cache(url):
	if url is None:
		return None
	data = None
	logger.info('Looking up %s', url)
	image_name = url.split('/').pop()
	with resources.cache.open(image_name, 'a+b') as f:
		logger.info('Opening %s', f.name)
		f.seek(0)
		data = f.read()
		if len(data) is 0:
			logger.info('Downloading: %s', url)
			data = urllib2.urlopen(url).read()
			f.write(data)
		return data
