import SCAN_LAN
from flask import Flask, request
import socket
import config
import threading
import server
app = Flask(__name__)

@app.route('/')
def hello_world():
    # return 'Hello World!'
    destination = SCAN_LAN.scan_port("localhost", 8888)
    if destination:
        return destination
    else:
        return "2"

@app.route('/ip')
def ip():
    ip = request.remote_addr
    return ip

@app.route('/hostname')
def hostname():
    return socket.gethostname()

if __name__ == '__main__':
    t = threading.Thread(target=server.server_run)
    t.setDaemon(True)
    t.start()
    app.run(host='0.0.0.0', port=config.app_port, threaded=True)
