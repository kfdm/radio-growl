__purple__ = __name__

import AnimeNFO.core
from purplebot.decorators import threaded, ratelimit


@ratelimit('RadioPlugin::ratelimit', 60)
@threaded
def playing(bot, hostmask, line):
	dest = line[2] if line[2][0:1] == '#' else hostmask['nick']

	playing = AnimeNFO.core.now_playing()
	message = '%s - %s - %s' % (playing.title, playing.artist, playing.album)
	bot.irc_privmsg(dest, message)

playing.command = '.playing'
