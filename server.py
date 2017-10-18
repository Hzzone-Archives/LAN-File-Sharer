import socket
import logging
import config
import SCAN_LAN

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S')

def server_run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((SCAN_LAN.get_internal_ip(), config.port))
    except socket.error as e:
        logging.error("socket create error: %s" % e)
    sock.listen(5)
    while True:
        conn, address = sock.accept()
        msg = conn.recv(1024)
        if msg:
            logging.debug('received from %s: %s' % (address, msg))
            # dic = json.loads(msg.decode())
            # if dic["type"] == "login":
            #     account = dic["account"]
            #     password = dic["password"]
            #     user = {account: password}
            #     if user in users:
            #         print("%s 登录成功" % account)
            #         sock.sendto("True".encode(), address)
            #     else:
            #         sock.sendto("False".encode(), address)
            # else:
            #     sock.sendto("服务器已接受消息".encode(), address)


if __name__ == "__main__":
    server_run()

