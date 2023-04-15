import SocketUdp
import File

class Server:
    def __init__(self, host, port, storage_path):
        self.socket = SocketUdp.SocketUdp(host, port)
        self.socket.bind()
        print("Esperando conexiones...")
        while True:
            protocol_message, addr = self.socket.receive()
            print(protocol_message)
            messages = protocol_message.decode().split("-")
            self.socket.sendto('g'.encode(), addr)
            rcv_data = 0
            file = File.File(storage_path + "/" + messages[2], messages[2])
            file.open('wb')
            while rcv_data < int(messages[1]):
                data, addr = self.socket.receive()
                rcv_data += len(data)
                print(rcv_data)
                file.write(data)
            file.close()
