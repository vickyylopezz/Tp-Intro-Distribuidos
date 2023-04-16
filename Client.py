from SocketUdp import SocketUdp
import File 

class Client:

    CHUNK_SIZE = 50000

    def __init__(self, server_host, server_port):
        self.server_address = (server_host, server_port)
        self.socket = SocketUdp()
        self.address = None
        self.file = None

    def send_operation(self, operation, fpath, fname):
        self.file = File.File(fpath, fname)
        if operation == "u":
            protocol_message = operation + '-' + str(self.file.size()) + '-' + fname
        else:
            protocol_message = operation + '-' + fname
        encoded_message = str.encode(protocol_message)
        self.socket.sendto(encoded_message, self.server_address)

    def wait_confirmation(self):
        confirmation, new_address = self.socket.receive()
        print(confirmation)
        self.address = new_address

    def receive(self):
        message, addr = self.socket.receive()
        print(message.decode())
        return message.decode(), addr

    def send_confirmation(self, addr):
        self.socket.sendto('g'.encode(), addr)

    def send_file(self):
        self.file.open("rb")
        while True:
            chunk = self.file.read(self.CHUNK_SIZE)
            if not chunk:
                break
            self.socket.sendto(chunk, self.address)

        self.file.close()

    def receive_file(self, length):
        rcv_data = 0
        self.file.open('wb')
        while rcv_data < int(length):
            data, addr = self.socket.receive()
            rcv_data += len(data)
            self.file.write(data)
        self.file.close()

