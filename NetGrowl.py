import gntp
import socket

class NetGrowl:
	def __init__(self,host=None,port=None,password=None,debug=False):
		self.host = host
		self.port = int(port)
		self.password = password
		self.debug = debug
	def _send(self,host,port,data,debug=False):
		if debug: print '<Sending>\n',data,'\n</Sending>'
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host,port))
		s.send(data)
		response = gntp.parse_gntp(s.recv(1024))
		s.close()
		if debug: print '<Recieving>\n',response,'\n</Recieving>'
	def register(self,name,title,icon):
		register = gntp.GNTPRegister(password=self.password)
		register.add_header('Application-Name',name)
		register.add_header('Application-Icon',icon)
		register.add_notification(title)
		
		try:
			self._send(self.host,self.port,register.encode(),self.debug)
		except IOError,e:
			print e
		except gntp.BaseError,e:
			print e
	def notice(self,name,notification,title,text,callback=None,image=None):
		notice = gntp.GNTPNotice(password=self.password)
		notice.add_header('Application-Name',name)
		notice.add_header('Notification-Name',notification)
		notice.add_header('Notification-Title',title)
		notice.add_header('Notification-Text',text)
		if image:
			notice.add_header('Notification-Icon',image)
		if callback:
			notice.add_header('Notification-Callback-Target',callback)
		
		try:
			self._send(self.host,self.port,notice.encode(),self.debug)
		except IOError,e:
			print e
		except gntp.BaseError,e:
			print e
