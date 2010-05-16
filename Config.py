import sys
import os
from ConfigParser import ConfigParser

class Config:
	def __init__(self,file):
		self._file = os.path.expanduser(file)
		self._config = ConfigParser()
		try: self._config.readfp(open(self._file))
		except IOError:
			print >> sys.stderr, 'No config file found.  Writing defaults to',file
			self._config.set('DEFAULT','host','###')
			self._config.set('DEFAULT','port','23053')
			self._config.set('DEFAULT','password','###')
			self._config.set('DEFAULT','appname','AnimeNFO')
			self._config.set('DEFAULT','title','Now Playing')
			self._config.set('DEFAULT','icon','http://www.animenfo.com/favicon.ico')
			self._config.write(open(self._file,'w'))
			sys.exit(1)
	def __getattr__(self,name):
		return self._config.get('DEFAULT',name)
	