import Config
import AnimeNFO
import NetGrowl

config	= Config.Config('~/.radio-growl')

growl = NetGrowl.NetGrowl(config.host,config.port,config.password)
growl.register(
	config.appname,
	config.title,
	config.icon
)

#Now Playing Strings
playing = AnimeNFO.now_playing()
title = '%s - %s - %s'%(playing.title,playing.artist,playing.album)
message = '[%s/%s]  Rating:[%s/10]'%(
	playing.duration[0],
	playing.duration[1],
	playing.rating
)

growl.notice(
	config.appname,
	config.title,
	title,
	message,
	AnimeNFO.PLAY_URL,
	playing.image
)
