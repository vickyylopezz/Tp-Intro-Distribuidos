import socket


class SocketUdp:
    def __init__(self, ip=None, port=None):
        self.ip = ip or "127.0.0.1"
        self.port = port or 8888
        # self.buffer = 50000
        self.buffer = 1472
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def timeout(self, time):
        self.socket.settimeout(time)

    def bind(self):
        self.socket.bind((self.ip, self.port))

    def receive(self):
        message, addr = self.socket.recvfrom(self.buffer)
        return message, addr

    def send(self, data):
        self.socket.sendto(data, (self.ip, self.port))

    def sendto(self, data, addr):
        self.socket.sendto(data, addr)

    def close(self):
        self.socket.close()
