import socket
import showtext
import os
import signal

IP = ""
PORT = 6666

FILE_NAME = "led-server.log"
MSG_SIZE = 1024

f = open("./"+FILE_NAME, 'a')
pid = 0

def decode(receivedString):
	global pid
	if pid != 0:
		os.kill(pid, signal.SIGKILL)
	showtext.clearLEDMatrix()
	myList = receivedString.split(";")
	if len(myList) == 3:
		myList[0] = "Song: "+myList[0]
		myList[1] = "Artist: "+myList[1]
		myList[2] = "Album: "+myList[2]
	myTupleList = list()
	for myString in myList:
		myTupleList.append(showtext.createTextColor(myString, (255, 0,0)))
		print( myString )
	pid = showtext.showOnLEDMatrix(tuple(myTupleList))
	print("")

def save(receivedString):
	f.write(receivedString+'\n')

clientSocket = None

try:
	print("ledserver.py started")
	#create an INET, STREAMing socket
	serverSocket = socket.socket(
		socket.AF_INET, socket.SOCK_STREAM)
	#bind the socket to a public host,
	# and a well-known port
	serverSocket.bind((IP, PORT))

	print("Listening")
	#become a server socket
	serverSocket.listen(1)

	(clientSocket, address) = serverSocket.accept()
	print("Accepted")
	while 1:
		clientRequest = clientSocket.recv(MSG_SIZE)
		if not clientRequest:
			break
		decode(clientRequest)
		save(clientRequest)
	clientSocket.close()
	f.close()

except KeyboardInterrupt:
	if clientSocket:
		clientSocket.close()
	if f:
		f.close()
	print("Closing")
if pid != 0:
	os.kill(pid, signal.SIGKILL)
showtext.clearLEDMatrix()