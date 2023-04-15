import SocketUdp

class Server:
    def __init__(self):
        self.socket = SocketUdp.SocketUdp()
        self.socket.bind()
        print("Esperando conexiones...")
        while(True):
            message, addr = self.socket.receive()
            print(message)
            self.socket.sendto('g'.encode(), addr)
        

        



    