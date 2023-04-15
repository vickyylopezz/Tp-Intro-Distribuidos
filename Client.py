import SocketUdp
import File 

class Client:

    CHUNK_SIZE = 50000

    def __init__(self, host, port):
        self.socket = SocketUdp.SocketUdp(host, port)
        self.file = None

    def send_operation(self, operation, fpath, fname):
        self.file = File.File(fpath, fname)
        if operation == "u":
            protocol_message = operation + '-' + str(self.file.size()) + '-' + fname
        else:
            protocol_message = operation + '-' + fname
        encoded_message = str.encode(protocol_message)
        self.socket.send(encoded_message)

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
            self.socket.send(chunk)

        self.file.close()

    def receive_file(self, length):
        rcv_data = 0
        self.file.open('wb')
        while rcv_data < int(length):
            data, addr = self.socket.receive()
            rcv_data += len(data)
            self.file.write(data)
        self.file.close()

