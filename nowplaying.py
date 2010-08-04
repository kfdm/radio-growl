#!/usr/bin/env python
import Config
import AnimeNFO
from gntp.notifier import GrowlNotifier

config	= Config.Config('~/.gntp')
growl = GrowlNotifier(
	applicationName = config['radio.appname'],
	notifications = [config['radio.title']],
	applicationIcon = config['radio.icon'],
	hostname = config['gntp.host'],
	password = config['gntp.password']
)
growl.debug = config['radio.debug']
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
	noteType=config['radio.title'],
	title=title,
	description=message,
	icon=playing.image,
	#callback=AnimeNFO.PLAY_URL,
)
