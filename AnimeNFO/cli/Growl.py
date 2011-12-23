import gntp.notifier
import logging


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
			logging.getLogger(__name__).exception('Is growl running ? Exiting....')
			exit()

	def alert(self, title, message, image):
		try:
			self.notify(
				noteType='Now Playing',
				title=title,
				description=message,
				icon=image,
				#callback=AnimeNFO.PLAY_URL,
				)
		except:
			logging.getLogger(__name__).exception('Is growl running ?')
