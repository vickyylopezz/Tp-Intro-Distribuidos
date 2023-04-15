import SocketUdp

class Client:
    def __init__(self):
        self.socket = SocketUdp.SocketUdp()

    def send(self):
        message = str.encode('Hello')
        self.socket.send(message)