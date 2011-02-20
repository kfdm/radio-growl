#!/usr/bin/env python
import AnimeNFO
import Growl
import time
	
def _to_seconds(time):
	time = time.split(':')
	return 60*int(time[0]) + int(time[1])

growl = Growl.GrowlNotifier()
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
			growl.alert(title,message,playing.image)
		try:	time_left = _to_seconds(playing.duration[0])
		except:	time_left = 20
		time.sleep(time_left+5)
	except KeyboardInterrupt:
		break
