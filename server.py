import Config
import AnimeNFO
import NetGrowl
import time
	
def _to_seconds(time):
	time = time.split(':')
	return 60*int(time[0]) + int(time[1])

config	= Config.Config('~/.radio-growl')

growl = NetGrowl.NetGrowl(config.host,config.port,config.password)
growl.register(
	config.appname,
	config.title,
	config.icon
)

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
		title = '%s - %s - %s'%(playing.title,playing.artist,playing.album)
		if title != previous:
			previous = title
			message = '[%s/%s]  Rating:[%s/10]'%(
						playing.duration[0],
						playing.duration[1],
						playing.rating
					)
			print title,message
			growl.notice(
				config.appname,
				config.title,
				title,
				message,
				AnimeNFO.PLAY_URL,
				playing.image
			)
		time_left = _to_seconds(playing.duration[0])
		print 'Sleepting for',time_left
		time.sleep(time_left+5)
	except KeyboardInterrupt:
		break