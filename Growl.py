import pydefaults
import gntp.notifier

gntp_settings = pydefaults.database('com.github.kfdm.gntp')
radio_settings = pydefaults.database('com.github.kfdm.radio')

class GrowlNotifier(gntp.notifier.GrowlNotifier):
	def __init__(self):
		self.applicationName = radio_settings['appname']
		self.notifications = [radio_settings['title']]
		self.defaultNotifications = self.notifications
		self.applicationIcon = radio_settings['icon']
		self.hostname = gntp_settings['host']
		self.password = gntp_settings['password']
		self.port = gntp_settings['port']
		self.debug = radio_settings['debug']
	def alert(self,title,message,image):
		self.notify(
			noteType=radio_settings['title'],
			title=title,
			description=message,
			icon=image,
			#callback=AnimeNFO.PLAY_URL,
		)
