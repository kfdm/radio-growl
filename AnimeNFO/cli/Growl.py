import gntp.config
import logging
from clint import resources
import urllib2

logger = logging.getLogger(__name__)


class GrowlNotifier(gntp.config.GrowlNotifier):
	def __init__(self):
		gntp.notifier.GrowlNotifier.__init__(
			self,
			applicationName='AnimeNFO Radio',
			notifications=['Now Playing'],
			applicationIcon='http://www.animenfo.com/favicon.ico',
		)

		resources.init('kfdm', 'radio-growl')

		try:
			self.register()
		except:
			logger.exception('Is growl running ? Exiting....')
			exit()

	def add_origin_info(self, packet):
		pass

	def alert(self, title, message, image, callback):
		data = None
		image_path = None
		image_name = image.split('/').pop()
		with resources.cache.open(image_name, 'w+') as f:
			logger.info('Opening %s', f.name)
			image_path = f.name
			data = f.read()
			if len(data) is 0:
				logger.info('Downloading: %s', image)
				data = urllib2.urlopen(image).read()
				f.write(data)
			else:
				data = f.read()

		try:
			self.notify(
				noteType='Now Playing',
				title=title,
				description=message,
				icon=data,
				callback=callback,
				)
		except:
			logger.exception('Is growl running ?')
