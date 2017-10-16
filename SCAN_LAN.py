import socket
import logging
import config
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

def scan_port(address, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0.1)
    s.connect_ex((address, port))
    # s.sendall("Hello world".encode())
    if s.connect_ex((address, port)) == 0:
        logging.debug("port scan, %s %s" % (address, port))
    else:
        return False
    s.close()
    return address, port


if __name__ == "__main__":
    scan_port("localhost", config.port)