import logging
import platform
import hashlib

import gntp.config

from AnimeNFO.cli import Cache
from AnimeNFO import __version__

logger = logging.getLogger(__name__)


class GrowlNotifier(gntp.config.GrowlNotifier):
	def __init__(self, use_cache=False):
		self.use_cache = use_cache

		image = 'http://www.animenfo.com/favicon.ico'
		if self.use_cache:
			image = Cache.image_cache(image)

		gntp.config.GrowlNotifier.__init__(
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
		"""Add optional Origin headers to message"""
		packet.add_header('Origin-Machine-Name', platform.node())
		packet.add_header('Origin-Software-Name', 'radio-growl')
		packet.add_header('Origin-Software-Version', __version__)
		packet.add_header('Origin-Platform-Name', platform.system())
		packet.add_header('Origin-Platform-Version', platform.platform())

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
		id = hashlib.md5(packet.headers['Notification-Title'].encode('utf-8')).hexdigest()
		packet.add_header('Notification-Coalescing-ID', id)
