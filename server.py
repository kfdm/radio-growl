from optparse import OptionParser
import socket
import AnimeNFO
import gntp
import time

def _send(host,port,data,debug=False):
	if debug: print '<Sending>\n',data,'\n</Sending>'
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	s.send(data)
	response = gntp.parse_gntp(s.recv(1024))
	s.close()
	if debug: print '<Recieving>\n',response,'\n</Recieving>'
	
def _to_seconds(time):
	time = time.split(':')
	return 60*int(time[0]) + int(time[1])

parser = OptionParser()
#Network
parser.add_option("-H","--hostname",dest="host",default="localhost")
parser.add_option("-p","--port",dest="port",help="port to send on",type="int",default=23053)
parser.add_option("-P","--password",dest="password",help="network password")

#Other
parser.add_option("-a","--appname",dest="app",default="AnimeNFO")
parser.add_option("-t","--title",dest="title",default="Now Playing")
parser.add_option("-d","--debug",dest='debug',help="Print raw growl packets",action="store_true",default=False)
(options, args) = parser.parse_args()

#Registration Message
print 'Registering App'
appicon = 'http://www.animenfo.com/favicon.ico'
register = gntp.GNTPRegister(password=options.password)
register.add_header('Application-Name',options.app)
register.add_header('Application-Icon',appicon)
register.add_notification(options.title)

try:
	_send(options.host,options.port,register.encode(),options.debug)
except IOError,e:
	print e
except gntp.BaseError,e:
	print e

previous = ''
while(1):
	try:
		#Now Playing Strings
		try:
			playing = AnimeNFO.now_playing()
		except IOError,e:
			print 'Timeout.  Sleeping for 20'
			time.sleep(20)
			continue
		title = '%s - %s - %s'%(playing.title,playing.artist,playing.album)
		title = unicode(title,'utf8')
		if title != previous:
			previous = title
			message = '[%s/%s]  Rating:[%s/10]'%(
						playing.duration[0],
						playing.duration[1],
						playing.rating
					)
			message = unicode(message,'utf8')
			print title
			print message
			#Notification
			notice = gntp.GNTPNotice(password=options.password)
			notice.add_header('Application-Name',options.app)
			notice.add_header('Notification-Name',options.title)
			notice.add_header('Notification-Title',title)
			notice.add_header('Notification-Text',message)
			if playing.image:
				notice.add_header('Notification-Icon',playing.image)
			notice.add_header('Notification-Callback-Target',AnimeNFO.PLAY_URL)
			
			try:
				_send(options.host,options.port,notice.encode(),options.debug)
			except IOError,e:
				print e
			except gntp.BaseError,e:
				print e
			except UnicodeEncodeError,e:
				print e
				print title
		time_left = _to_seconds(playing.duration[0])
		print 'Sleepting for',time_left
		time.sleep(time_left+5)
	except KeyboardInterrupt:
		break