import socket
import threading
import config

class Send_Single_File_Thread(threading.Thread):

    def __init__(self, ip, port, file_path):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.file_path = file_path

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        with open(self.file_path, 'rb') as f:
            for data in f:
                s.send(data)
        s.close()

    def get_result(self):
        return self.result

if __name__ == "__main__":
    pass
