#!/usr/bin/env python
import pydefaults
import AnimeNFO
from gntp.notifier import GrowlNotifier

gntp = pydefaults.database('com.github.kfdm.gntp')
radio = pydefaults.database('com.github.kfdm.radio')

growl = GrowlNotifier(
	applicationName = radio['appname'],
	notifications = [radio['title']],
	applicationIcon = radio['icon'],
	hostname = gntp['host'],
	password = gntp['password'],
	port = gntp['port']
)
growl.debug = radio['debug']
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
