import SocketUdp

class Server:
    def __init__(self):
        self.socket = SocketUdp.SocketUdp()
        self.socket.bind()
        print("Esperando conexiones...")
        while(True):
            message, addr = self.socket.receive()
            print(message)
            messages = message.split("-")
            self.socket.sendto('g'.encode(), addr)
            rcv_data = 0
            while(rcv_data < int(messages[1])):
                self.socket.receive()
        

        



    