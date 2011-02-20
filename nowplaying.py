#!/usr/bin/env python
import AnimeNFO
import Growl

growl = Growl.GrowlNotifier()
growl.register()

#Now Playing Strings
playing = AnimeNFO.now_playing()
title = u'%s - %s - %s'%(playing.title,playing.artist,playing.album)
message = u'[%s/%s]  Rating:[%s/10]'%(
	playing.duration[0],
	playing.duration[1],
	playing.rating
)

growl.alert(title,message,playing.image)
