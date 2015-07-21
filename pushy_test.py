
import pushybullet as pb
import serial
import time
import zmq
import random
import sys
import threading
import unicodedata

API_KEY 		= 	'WriteYourAPIKey'
D_SYNC 			=	0.2
NORMALIZATION 	=	'NFKD'
SERIAL			=	'/dev/ttyUSB2'

def check_socket():
	while True:
		msg = socket.recv_string()
		print(msg)
#		socket.send_string("Server message to client: 1")	

port = "0000"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)
    
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" %port)
#socket.connect("tcp://*:%s" %port)

class LastPush:
	def __init__(self, push_time, push_type, push_iden):
		self.time = push_time
		self.type = push_type
		self.iden = push_iden


last_push = LastPush(time.time(), 'none', 'none')

first_launch=True

def normalize_str(str_to_normalize):
	return str_to_normalize.encode('ascii', 'ignore')

def send_serial(command, send_str):
	ret_str = bytes(";"+command+"="+normalize_str(send_str)+'\n')
	print "command: ", bytes(";"+command+"="+normalize_str(send_str)+'\n')
	ser.write(ret_str)
	time.sleep(D_SYNC)
	return ret_str

def check_push():
#	ser = serial.Serial('/dev/ttyUSB0', 9600)
#	ser.write(";P=TEsT")
#	send_serial("P", "TEsT")
	send_serial("p", "")
	send_serial("P", "No new message")
	for event in api.stream():	

		print'\n',("Event: ", event)
		print("Event class name: ", event.__class__.__name__)
		print("Event time: ", event.latest_push_time())

		for push in event.pushes():
			print'\n',("Push class name: ", push.__class__.__name__)
			push_type = push.__class__.type
			print("Push class type: ", push_type)
			
			if(push_type == 'dismissal'):
				print'\n',("Dismissal")
				
			elif(push_type == 'mirror'):
				print("Push title: ", push.title)
				print("Title normalized: ", normalize_str(push.title))
				send_serial("p", push.title)
				time.sleep(D_SYNC)
				print("Push body: ", push.body)
				print("Body normalized: ", normalize_str(push.body))
				send_serial("P", push.body)
				
			elif(push_type == 'note'):
				if(push.iden != last_push.iden):				
					print("Push iden: ", push.iden)
					print("Last push iden: ", last_push.iden)
					last_push.iden = push.iden
					print("Push title: ", push.title)
					send_serial("p", push.title)
					time.sleep(D_SYNC)
					print("Push body: ", push.body)
					send_serial("P", push.body)
										
			elif(push_type == 'link'):
				if(push.iden != last_push.iden):				
					print("Push iden: ", push.iden)
					print("Last push iden: ", last_push.iden)
					last_push.iden = push.iden
					print("Push title: ", push.title)
					send_serial("p", push.title)
					time.sleep(D_SYNC)
					print("Push body: ", push.body)
					send_serial("P", push.body)
					print("Push url: ", push.url)
					send_serial("P", push.url)
					
			elif(push_type == 'file'):
				if(push.iden != last_push.iden):				
					print("Push iden: ", push.iden)
					print("Last push iden: ", last_push.iden)
					last_push.iden = push.iden
					print("Push title: ", push.title)
					print("Push filename: ", push.file_name)
					send_serial("p", push.file_name)
					time.sleep(D_SYNC)
					print("Push body: ", push.body)
#					ser.write(bytes(";P="+push.body))
					print("Push type: ", push.file_type)
					send_serial("P", push.file_type)
					
				

api = pb.PushBullet(API_KEY)

devices = api.devices()

dev_chrome = api['Chrome']
dev_n5 = api['LGE Nexus 5']
dev_ff = api['Firefox']

#api.stream(skip_nop=False)
#api.stream(use_server_time=True)
#print devices
print dev_chrome, "\n", dev_n5, "\n", dev_ff

#ser = serial.Serial(SERIAL, 9600)


#push = pb.NotePush("New test", "Hello")
#push.send(dev_n5)

#dev_chrome.push("Hi, this is a test")


ser = serial.Serial(SERIAL, 9600)
ser.write(";P=TEsT\n")

check_push_thread = threading.Thread(target=check_push)
check_push_thread.daemon = True
check_push_thread.start()

check_socket_thread = threading.Thread(target=check_socket)
check_socket_thread.daemon = True
check_socket_thread.start()

while True:
	time.sleep(1)

	
	
		

