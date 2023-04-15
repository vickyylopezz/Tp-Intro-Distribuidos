import SocketUdp

class Server:
    def __init__(self):
        self.socket = SocketUdp.SocketUdp()
        self.socket.bind()
        print("Esperando conexiones...")
        self.socket.receive()
        

        



    