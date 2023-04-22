import socket
import SelectiveRepeat
import StopAndWait
from Logging import Logging
from SocketUdp import SocketUdp
from File import File
import threading

class Server:

    def __init__(self, host, port, storage_path, transport_protocol):
        self.socket = SocketUdp(host, port)
        self.socket.bind()
        self.storage = storage_path
        self.active = False
        self.main_thread = None
        self.threads = []
        self.transport_protocol = transport_protocol
        self.log = Logging()

    def start(self):
        self.log.info('Inicio server')
        self.main_thread = threading.Thread(target=self.listen)
        self.main_thread.start()

    def stop(self):
        self.active = False
        self.main_thread.join()
        self.log.info('Fin server')

    def listen(self):
        self.active = True
        self.log.info('Esperando clientes')
        while self.active:
            self.socket.timeout(5)
            try:
                protocol_message, addr = self.socket.receive()
                self.log.info('Atendiendo cliente', addr)
                client_thread = threading.Thread(target=self.handle_client, args=(protocol_message, addr))
                client_thread.start()
                self.threads.append(client_thread)
            except socket.timeout:
                continue
        for t in self.threads:
            t.join()

    def handle_client(self, message, address):
        print(message)
        messages = message.decode().split("-")
        if messages[0] == "u":
            self.handle_upload(address, self.storage, messages)
        if messages[0] == "d":
            self.handle_download(address, self.storage, messages)

    def handle_upload(self, addr, storage_path, messages):
        client_socket = SocketUdp()
        self.log.info("Enviamos confirmacion", addr)
        client_socket.sendto('g'.encode(), addr)
        file = File(storage_path + "/" + messages[2], messages[2])
        file.open('wb')
        if(self.transport_protocol == "saw"):
            protocol = StopAndWait.StopAndWait(client_socket)
        elif(self.transport_protocol == "sr"):
            protocol = SelectiveRepeat.SelectiveRepeat(client_socket)
        protocol.receive(file, int(messages[1]))
        file.close()
        client_socket.close()

    def handle_download(self, addr, storage_path, messages):
        client_socket = SocketUdp()
        file = File(storage_path + "/" + messages[1], messages[1])
        client_socket.sendto(str(file.size()).encode(), addr)
        print("esperando confirmacion")
        # deberia haber un timeout por si se cae la longitud o la conf del cliente
        client_socket.timeout(5)
        try:
            confirmation, addr = client_socket.receive()
            print("llego la confirmacion, comienza transferencia")
        except:
            print("No recibi confirmacion, desconectando")
            client_socket.close()
            return # ?
        file.open("rb")
        # while True:
        #     chunk = file.read(self.CHUNK_SIZE)
        #     if not chunk:
        #         break
        #     self.socket.sendto(chunk, addr)

        if(self.transport_protocol == "saw"):
            protocol = StopAndWait.StopAndWait(client_socket)
        elif(self.transport_protocol == "sr"):
            protocol = SelectiveRepeat.SelectiveRepeat(client_socket)
        
        # protocol = SelectiveRepeat.SelectiveRepeat(client_socket)
        # protocol = StopAndWait.StopAndWait(client_socket)
        protocol.send(file, addr)

        file.close()
        client_socket.close()
