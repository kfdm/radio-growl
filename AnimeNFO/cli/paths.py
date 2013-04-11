import os
import platform

__all__ = ['PID_PATH', 'LOG_PATH']

OS = platform.system()
HOME = os.path.expanduser('~')

if OS == 'Darwin':
	CACHE_PATH = os.path.join(
		HOME, 'Library', 'Caches', 'radio-growl'
	)
	PID_PATH = os.path.join(
		CACHE_PATH, 'daemon.pid'
	)
	LOG_PATH = os.path.join(
		HOME, 'Library', 'Logs', 'radio.log'
	)
