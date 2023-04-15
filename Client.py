import SocketUdp
import File 

class Client:

    CHUNK_SIZE = 50000

    def __init__(self, host, port):
        self.socket = SocketUdp.SocketUdp(host, port)
        self.file = None

    def send_operation(self, fpath, fname):
        self.file = File.File(fpath, fname)
        protocol_message = 'u' + '-' + str(self.file.size()) + '-' + fname
        encoded_message = str.encode(protocol_message)
        self.socket.send(encoded_message)

    def receive(self):
        message, addr = self.socket.receive()
        print(message.decode())

    def send_file(self):
        self.file.open("rb")
        while True:
            chunk = self.file.read(self.CHUNK_SIZE)
            if not chunk:
                break
            self.socket.send(chunk)

        self.file.close()

