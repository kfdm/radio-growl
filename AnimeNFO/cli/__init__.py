#!/usr/bin/env python

import time
import logging
import optparse
import os

import AnimeNFO
from AnimeNFO.cli import Growl, daemon

LOG_FORMAT  = '%(asctime)s %(levelname)-8s %(name)-12s %(message)s'
DEFAULT_PID = os.path.realpath('./radio.pid')
DEFAULT_LOG = os.path.realpath('./radio.log')

class Parser(optparse.OptionParser):
	def __init__(self):
		def store_path(option, opt, value, parser):
			setattr(parser.values, option.dest, os.path.realpath(value))

		optparse.OptionParser.__init__(self, usage="%prog [options] (start|stop|restart)")
		self.add_option('-p', '--pid', dest='pid', default=DEFAULT_PID,
			action='callback', callback=store_path, type=str)
		self.add_option('-l', '--log', dest='log', default=DEFAULT_LOG,
			action='callback', callback=store_path, type=str)
		self.add_option('-v', '--verbose', dest='verbose', default=logging.INFO,
			action='store_const', const=logging.DEBUG)

class Radio(daemon.Daemon):
	def run(self, loop=True):
		def to_seconds(time):
			try:
				time = time.split(':')
				return 60 * int(time[0]) + int(time[1])
			except:
				return 20

		def now_playing():
			while(1):
				try:
					return AnimeNFO.now_playing()
				except IOError:
					logging.debug('Timeout.  Sleeping for 20')
					time.sleep(20)
		growl = Growl.GrowlNotifier()
		previous = ''
		while(True):
			playing = now_playing()
			title = u'%s - %s - %s' % (playing.title, playing.artist, playing.album)
			if title != previous:
				message = u'[%s/%s]  Rating:[%s/10]' % (
							playing.duration[0],
							playing.duration[1],
							playing.rating
						)
				logging.info('%s %s', title, message)
				growl.alert(title, message, playing.image)
			if not loop:
				break
			time_left = to_seconds(playing.duration[0])
			logging.debug('Sleeping for %d', time_left)
			time.sleep(time_left + 5)

(options, args) = Parser().parse_args()
radio = Radio(options.pid)

def main():
	try:
		import setproctitle
		setproctitle.setproctitle('radio-growl')
	except ImportError:
		pass

	if 'start' in args:
		logging.basicConfig(
			level=options.verbose,
			filename=options.log,
			format=LOG_FORMAT
		)
		radio.start()
	elif 'restart' in args:
		logging.basicConfig(
			level=options.verbose,
			filename=options.log,
			format=LOG_FORMAT
		)
		radio.restart()
	elif 'stop' in args:
		radio.stop()
	else:
		logging.basicConfig(level=options.verbose, format=LOG_FORMAT)
		radio.run(False)

if __name__ == '__main__':
	main()
