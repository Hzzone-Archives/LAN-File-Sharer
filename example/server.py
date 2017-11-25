import socket
import logging
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S')
s.bind(('localhost', 8888))    #ip地址和端口号
s.listen(5)
while True:
    conn, address = s.accept()
    msg = conn.recv(1024)
    if msg:
        logging.debug('received from %s: %s' % (address, msg))
        conn.sendall("hh".encode())
