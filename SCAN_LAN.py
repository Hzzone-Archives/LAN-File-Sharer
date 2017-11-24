import socket
import logging
import config
import os
from functools import reduce
import threading
import time
import requests
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

def ip_into_int(ip):
    # 先把 192.168.1.13 变成16进制的 c0.a8.01.0d ，再去了“.”后转成10进制的 3232235789 即可。
    # (((((192 * 256) + 168) * 256) + 1) * 256) + 13
    return reduce(lambda x, y: (x << 8) + y, map(int, ip.split('.')))

'''
判断是否是内网ip
'''
def is_internal_ip(ip):
    ip = ip_into_int(ip)
    net_a = ip_into_int('10.255.255.255') >> 24
    net_b = ip_into_int('172.31.255.255') >> 20
    net_c = ip_into_int('192.168.255.255') >> 16
    return ip >> 24 == net_a or ip >> 20 == net_b or ip >> 16 == net_c


'''
扫描给定的ip, 端口是否存活
'''
def scan_port(address, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    if s.connect_ex((address, port)) == 0:
        logging.debug("port scan, %s %s" % (address, port))
    else:
        return False
    s.close()
    return address

'''
获取本机内网ip地址
'''
def get_internal_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    logging.debug("Get local ip: " + ip)
    return ip

'''
多线程扫描内网的第一个网段
'''
class MyThread(threading.Thread):

    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = ip

    def run(self):
        self.result = scan_port(self.ip, config.port)

    def get_result(self):
        return self.result

'''
开始扫描整个局域网
返回所有可用的ip地址
'''
def scan_lan():
    local_ip = get_internal_ip()
    t = '.'.join(local_ip.split('.')[:3])
    temp = [t+'.'+str(x) for x in list(range(256))]
    threads = [MyThread(ip) for ip in temp]
    for t in threads:
        t.start()
    time.sleep(5)
    temp = [t.get_result() for t in threads]
    alive_addr = []
    for x in temp:
        if x:
            alive_addr.append(x)
    logging.debug("scanned alive ip address " + str(alive_addr))
    return alive_addr



if __name__ == "__main__":
    # scan_port("192.168.1.157", config.port)
    # address = scan_lan()[0]
    # print(scan_lan())
    # print(socket.gethostbyaddr("10.132.50.123"))
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.settimeout(0.1)
    # s.connect_ex((address, port))
    # print(s.connect_ex((address, port)))
    # s.connect((get_internal_ip(), config.port))
    # s.sendall("Hello world".encode())
    pass
