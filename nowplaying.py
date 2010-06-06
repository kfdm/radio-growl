#!/usr/bin/env python
import Config
import AnimeNFO
from gntp.notifier import GrowlNotifier

config	= Config.Config('~/.radio-growl')
growl = GrowlNotifier(
	applicationName = config.appname,
	notifications = [config.title],
	applicationIcon = config.icon,
	hostname = config.host,
	password = config.password
)
growl.register()

#Now Playing Strings
playing = AnimeNFO.now_playing()
title = u'%s - %s - %s'%(playing.title,playing.artist,playing.album)
message = u'[%s/%s]  Rating:[%s/10]'%(
	playing.duration[0],
	playing.duration[1],
	playing.rating
)

growl.notify(
	noteType=config.title,
	title=title,
	description=message,
	icon=playing.image,
	#callback=AnimeNFO.PLAY_URL,
)
