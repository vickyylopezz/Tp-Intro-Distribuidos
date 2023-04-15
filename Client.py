import SocketUdp
import File 

class Client:
    def __init__(self, host, port):
        self.socket = SocketUdp.SocketUdp(host, port)


    def send(self, fpath, fname):
        size = File.File(fpath, fname).size()
        message = 'u' + '-' + str(size) + '-' + fname
        encodedMessage = str.encode(message)
        self.socket.send(encodedMessage)

    def receive(self):
        message, addr = self.socket.receive()
        print(message)
