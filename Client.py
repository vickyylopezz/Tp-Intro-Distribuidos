import StopAndWait
from SocketUdp import SocketUdp
import File 

class Client:

    # CHUNK_SIZE = 50000

    def __init__(self, server_host, server_port):
        self.server_address = (server_host, server_port)
        self.socket = SocketUdp()
        self.address = None
        self.file = None
        self.protocol_message = None

    def send_operation(self, operation, fpath, fname):
        self.file = File.File(fpath, fname)
        if operation == "u":
            self.protocol_message = operation + '-' + str(self.file.size()) + '-' + fname
        else:
            self.protocol_message = operation + '-' + fname
        encoded_message = str.encode(self.protocol_message)
        self.socket.sendto(encoded_message, self.server_address)

    def wait_confirmation(self):
        timeouts = 0
        print(self.server_address)
        while timeouts < 5:
            print("Intento numero: " + str(timeouts + 1))
            self.socket.timeout(2)
            try:
                confirmation, new_address = self.socket.receive()
                print(confirmation)
                print(new_address)
                self.address = new_address
                return True
            except:
                timeouts += 1
                self.socket.sendto(self.protocol_message.encode(), self.server_address)

        return False

    def receive(self):
        message, addr = self.socket.receive()
        print(message.decode())
        return message.decode(), addr

    def send_confirmation(self, addr):
        self.socket.sendto('g'.encode(), addr)

    def send_file(self):
        self.file.open("rb")
        # while True:
        #     chunk = self.file.read(self.CHUNK_SIZE)
        #     if not chunk:
        #         break
        #     self.socket.sendto(chunk, self.address)

        protocol = StopAndWait.StopAndWait(self.socket)
        protocol.send(self.file, self.address)

        self.file.close()
        self.socket.close()

    def receive_file(self, length):
        rcv_data = 0
        self.file.open('wb')
        while rcv_data < int(length):
            data, addr = self.socket.receive()
            rcv_data += len(data)
            self.file.write(data)
        self.file.close()

    def close_socket(self):
        self.socket.close()