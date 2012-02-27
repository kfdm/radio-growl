#!/usr/bin/env python

import logging
logger = logging.getLogger(__name__)

import time
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
		self.add_argument('--cache', dest='use_cache', action='store_true')
		self.add_argument('daemon', nargs='?', choices=['start', 'stop', 'restart'])


class Radio(daemon.Daemon):
	def run(self, loop=True, use_cache=False):
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
					logger.debug('Timeout.  Sleeping for 20')
					time.sleep(20)
		growl = Growl.GrowlNotifier(self.options.use_cache)
		previous = ''
		while(True):
			playing = now_playing()
			title = TITLE_FORMAT.format(s=playing)
			if title != previous:
				message = INFO_FORMAT.format(s=playing)
				logger.info('%s %s', title, message)
				growl.alert(title, message, playing.image, AnimeNFO.API_URL)
			if not loop:
				break
			time_left = to_seconds(playing.duration[0])
			logger.debug('Sleeping for %d', time_left)
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
	radio.options = options

	if options.daemon is None:
		logging.basicConfig(level=options.verbose, format=LOG_FORMAT)
		radio.run(False, options.use_cache)
	else:
		logging.basicConfig(level=options.verbose, format=LOG_FORMAT, filename=options.log)
		if options.daemon == 'start':
			radio.start()
		elif options.daemon == 'restart':
			radio.restart()
		elif options.daemon == 'stop':
			radio.stop()

if __name__ == '__main__':
	main()
