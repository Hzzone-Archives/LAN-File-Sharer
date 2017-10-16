import SCAN_LAN
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    # return 'Hello World!'
    destination = SCAN_LAN.scan_port("localhost", 8888)
    if destination:
        return destination
    else:
        return "2"

if __name__ == '__main__':
    app.run()
