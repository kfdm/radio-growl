from gntp.config import Config

class RadioConfig(Config):
	_defaults = {
		'gntp':{
			'host':'localhost',
			'port':23053,
			'password':'',
		},
		'radio':{
			'appname':'AnimeNFO',
			'title':'Now Playing',
			'icon':'http://www.animenfo.com/favicon.ico',
			'debug':False,
		},
	}
	_booleans = ['radio.debug']
	_ints = ['gntp.port']
