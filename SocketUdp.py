import socket

class SocketUdp:
    def __init__(self, ip=None, port=None):
        self.ip = ip or '127.0.0.1'
        self.port = port or 8888
        self.buffer = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def bind(self):
        self.socket.bind((self.ip, self.port))

    def receive(self):
        while(True):
            message = self.socket.recvfrom(self.buffer)
            print(message)

    def send(self, data):
        self.socket.sendto(data, (self.ip, self.port))

    def close(self):
        self.socket.close()
