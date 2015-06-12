import logging
logger = logging.getLogger(__name__)
import urllib.request, urllib.error, urllib.parse
from clint import resources
from PIL import Image

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
			data = urllib.request.urlopen(url).read()
			f.write(data)
			f.flush()

			if not f.name.endswith('.ico'):
				logger.info('Resizing: %s', image_name)
				img = Image.open(f.name)
				img = img.resize((150, 150), Image.ANTIALIAS)
				img.save(f.name)

				# Reload the image
				data = open(f.name).read()

	return data
