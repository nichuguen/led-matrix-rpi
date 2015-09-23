
from localconstants import list_ips as list_ips
import requests

class Dispatcher:
	list_addresses_raw = [ ip + ":5000/" for ip in list_ips ]
	
	@staticmethod
	def send_song(song):
		payload = dict(song)
		payload['type'] = "song"
		Dispatcher.broadcast_to_pis("", payload)
		
	@staticmethod
	def send_stop():
		payload = {'type' : 'stop'}
		Dispatcher.broadcast_to_pis("", payload)
		
	@staticmethod
	def send_message(message):
		payload = {'type' : 'stop', 'message' : message}
		Dispatcher.broadcast_to_pis("", payload)
		
	@staticmethod
	def broadcast_to_pis(address_postfix, data):
		for address in Dispatcher.list_addresses_raw:
			requests.post(address+address_postfix, data=data)
		
