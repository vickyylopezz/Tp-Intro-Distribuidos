import SocketUdp
import File


class Server:

    CHUNK_SIZE = 50000

    def __init__(self, host, port, storage_path):
        self.socket = SocketUdp.SocketUdp(host, port)
        self.socket.bind()
        print("Esperando conexiones...")
        while True:
            protocol_message, addr = self.socket.receive()
            print(protocol_message)
            messages = protocol_message.decode().split("-")
            if messages[0] == "u":
                self.handle_upload(addr, storage_path, messages)
            if messages[0] == "d":
                self.handle_download(addr, storage_path, messages)
            # self.socket.sendto('g'.encode(), addr)
            # rcv_data = 0
            # file = File.File(storage_path + "/" + messages[2], messages[2])
            # file.open('wb')
            # while rcv_data < int(messages[1]):
            #    data, addr = self.socket.receive()
            #    rcv_data += len(data)
            #    file.write(data)
            # file.close()

    def handle_upload(self, addr, storage_path, messages):
        self.socket.sendto('g'.encode(), addr)
        rcv_data = 0
        file = File.File(storage_path + "/" + messages[2], messages[2])
        file.open('wb')
        while rcv_data < int(messages[1]):
            data, addr = self.socket.receive()
            rcv_data += len(data)
            file.write(data)
        file.close()

    def handle_download(self, addr, storage_path, messages):
        file = File.File(storage_path + "/" + messages[1], messages[1])
        self.socket.sendto(str(file.size()).encode(), addr)
        confirmation, addr = self.socket.receive()
        print(confirmation)
        file.open("rb")
        while True:
            chunk = file.read(self.CHUNK_SIZE)
            if not chunk:
                break
            self.socket.sendto(chunk, addr)

        file.close()
