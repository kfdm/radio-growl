import gntp.notifier
import logging

logger = logging.getLogger(__name__)


class GrowlNotifier(gntp.notifier.GrowlNotifier):
	def __init__(self):
		gntp.notifier.GrowlNotifier.__init__(
			self,
			applicationName='AnimeNFO Radio',
			notifications=['Now Playing'],
			applicationIcon='http://www.animenfo.com/favicon.ico',
		)

		try:
			self.register()
		except:
			logger.exception('Is growl running ? Exiting....')
			exit()

	def add_origin_info(self, packet):
		pass

	def alert(self, title, message, image, callback):
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
