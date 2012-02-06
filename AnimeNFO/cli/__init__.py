#!/usr/bin/env python

import time
import logging
import argparse
import os

import AnimeNFO
from AnimeNFO.cli import Growl, daemon

LOG_FORMAT = "%(asctime)s\t%(levelname)8s\t%(name)-12s\t%(message)s"
DEFAULT_PID = os.path.realpath('./radio.pid')
DEFAULT_LOG = os.path.realpath('./radio.log')

TITLE_FORMAT = u'{s.title} - {s.artist} - {s.album}'
INFO_FORMAT = u'[{s.duration[0]}/{s.duration[1]}  Rating:[{s.rating}/10]'


class Parser(argparse.ArgumentParser):
	def __init__(self):
		def store_path(value):
			return os.path.realpath(value)

		argparse.ArgumentParser.__init__(self)
		self.add_argument('-p', '--pid', default=DEFAULT_PID, type=store_path)
		self.add_argument('-l', '--log', default=DEFAULT_LOG, type=store_path)
		self.add_argument('-v', '--verbose', action='count', default=0)
		self.add_argument('daemon', nargs='?', choices=['start', 'stop', 'restart'])


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
			title = TITLE_FORMAT.format(s=playing)
			if title != previous:
				message = INFO_FORMAT.format(s=playing)
				logging.info('%s %s', title, message)
				growl.alert(title, message, playing.image, AnimeNFO.PLAY_URL)
			if not loop:
				break
			time_left = to_seconds(playing.duration[0])
			logging.debug('Sleeping for %d', time_left)
			time.sleep(time_left + 5)


def main():
	try:
		import setproctitle
		setproctitle.setproctitle('radio-growl')
	except ImportError:
		pass

	options = Parser().parse_args()
	options.verbose = logging.WARNING - options.verbose * 10
	radio = Radio(options.pid)

	if options.daemon == 'start':
		logging.basicConfig(
			level=options.verbose,
			filename=options.log,
			format=LOG_FORMAT
		)
		radio.start()
	elif options.daemon == 'restart':
		logging.basicConfig(
			level=options.verbose,
			filename=options.log,
			format=LOG_FORMAT
		)
		radio.restart()
	elif options.daemon == 'stop':
		radio.stop()
	else:
		logging.basicConfig(level=options.verbose, format=LOG_FORMAT)
		radio.run(False)

if __name__ == '__main__':
	main()
