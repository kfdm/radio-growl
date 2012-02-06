import logging
logger = logging.getLogger(__name__)
import gntp.config
import hashlib
from AnimeNFO.cli import Cache


class GrowlNotifier(gntp.config.GrowlNotifier):
	def __init__(self, use_cache=False):
		self.use_cache = use_cache

		image = 'http://www.animenfo.com/favicon.ico'
		if self.use_cache:
			image = Cache.image_cache(image)

		gntp.notifier.GrowlNotifier.__init__(
			self,
			applicationName='AnimeNFO Radio',
			notifications=['Now Playing'],
			applicationIcon=image,
		)

		try:
			self.register()
		except:
			logger.exception('Is growl running ? Exiting....')
			exit()

	def add_origin_info(self, packet):
		pass

	def alert(self, title, message, image, callback):
		if self.use_cache:
			image = Cache.image_cache(image)

		try:
			self.notify(
				noteType='Now Playing',
				title=title,
				description=message,
				icon=image,
				callback=callback,
				)
		except:
			logger.exception('Is growl running ?')

	def notify_hook(self, packet):
		id = hashlib.md5(packet.headers['Notification-Title']).hexdigest()
		packet.add_header('Notification-Coalescing-ID', id)
