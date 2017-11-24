import socket
import logging
import time
import threading

def send(sock, msg):
	sock.sendall(msg.encode())
	logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S')
for x in range(10):
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('localhost', 8888))
	threading.Thread(target=send, args=(s, str(x))).start()
	threading.Thread(target=send, args=(s, str(x))).start()
	# s.sendall("Hello world".encode())

time.sleep(10)
