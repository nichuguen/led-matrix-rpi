
from localconstants import list_ips as list_ips
import requests

class Dispatcher:
	
	list_addresses_raw = [ ip + ":5000/" for ip in list_ips ]
	
	@staticmethod
	def send_song(song):
		pass
		
	@staticmethod
	def send_stop():
		pass
		
	@staticmethod
	def send_message(message):
		pass
