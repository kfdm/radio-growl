import pydefaults
import gntp.notifier
import logging

radio_settings = pydefaults.database('com.github.kfdm.radio')

class GrowlNotifier(gntp.notifier.GrowlNotifier):
	def __init__(self):
		self.applicationName = radio_settings['appname']
		self.notifications = [radio_settings['title']]
		self.defaultNotifications = self.notifications
		self.applicationIcon = radio_settings['icon']
		self.hostname = radio_settings['host']
		self.password = radio_settings['password']
		self.port = int(radio_settings['port'])
		self.debug = radio_settings['debug']
		
		try:
			self.register()
		except:
			logging.getLogger(__name__).exception('Is growl running ? Exiting....')
			exit()
			
	def alert(self,title,message,image):
		try:
			self.notify(
				noteType=radio_settings['title'],
				title=title,
				description=message,
				icon=image,
				#callback=AnimeNFO.PLAY_URL,
				)
		except:
			logging.getLogger(__name__).exception('Is growl running ?')