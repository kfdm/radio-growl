import Config
import AnimeNFO
from gntp_notifier import GrowlNotifier
import time
	
def _to_seconds(time):
	time = time.split(':')
	return 60*int(time[0]) + int(time[1])

config	= Config.Config('~/.radio-growl')

growl = GrowlNotifier(
	applicationName = config.appname,
	notifications = [config.title],
	applicationIcon = config.icon,
	hostname = config.host,
	password = config.password
)
growl.register()

previous = ''
while(1):
	try:
		#Now Playing Strings
		try:
			playing = AnimeNFO.now_playing()
		except IOError,e:
			print 'Timeout.  Sleeping for 20'
			time.sleep(20)
			continue
		title = u'%s - %s - %s'%(playing.title,playing.artist,playing.album)
		if title != previous:
			previous = title
			message = u'[%s/%s]  Rating:[%s/10]'%(
						playing.duration[0],
						playing.duration[1],
						playing.rating
					)
			print title,message
			growl.notify(
				noteType=config.title,
				title=title,
				description=message,
				icon=playing.image,
				#callback=AnimeNFO.PLAY_URL,
			)
		time_left = _to_seconds(playing.duration[0])
		print 'Sleepting for',time_left
		time.sleep(time_left+5)
	except KeyboardInterrupt:
		break