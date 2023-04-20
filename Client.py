import socket

import SelectiveRepeat
import StopAndWait
from Logging import Logging
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
        log = Logging()
        log.log('Enviamos operacion')
        self.file = File.File(fpath, fname)
        if operation == "u":
            self.protocol_message = operation + '-' + str(self.file.size()) + '-' + fname
        else:
            self.protocol_message = operation + '-' + fname
        encoded_message = str.encode(self.protocol_message)
        self.socket.sendto(encoded_message, self.server_address)

    def wait_confirmation(self):
        log = Logging()
        timeouts = 0
        log.log('Esperamos confirmacion')
        while timeouts < 5:
            log.log("Intento numero: " + str(timeouts + 1))
            self.socket.timeout(2)
            try:
                confirmation, new_address = self.socket.receive()
                log.log('Recibimos confirmacion')
                self.address = new_address
                return True
            except socket.timeout:
                timeouts += 1
                self.socket.sendto(self.protocol_message.encode(), self.server_address)

        return False

    def receive_length(self):
        # length, addr = self.socket.receive()
        # print(length.decode())
        # return length.decode(), addr
        log = Logging()
        timeouts = 0
        log.log('Esperamos longitud del archivo')
        while timeouts < 5:
            log.log("Intento numero: " + str(timeouts + 1))
            self.socket.timeout(2)
            try:
                length, new_address = self.socket.receive()
                log.log('Recibimos longitud')
                self.address = new_address
                return length
            except socket.timeout:
                timeouts += 1
                self.socket.sendto(self.protocol_message.encode(), self.server_address)

        return 0

    def send_confirmation(self):
        # podria haber un intento de reenviar la confirmacion
        print("envio confirmacion")
        self.socket.sendto('g'.encode(), self.address)
        print("confirmacion enviada")

    def send_file(self):
        log = Logging()
        log.log("Enviamos archivo")
        self.file.open("rb")
        # while True:
        #     chunk = self.file.read(self.CHUNK_SIZE)
        #     if not chunk:
        #         break
        #     self.socket.sendto(chunk, self.address)

        protocol = StopAndWait.StopAndWait(self.socket)
        #protocol = SelectiveRepeat.SelectiveRepeat(self.socket)
        protocol.send(self.file, self.address)

        self.file.close()
        self.socket.close()

    def receive_file(self, length):
        # rcv_data = 0
        self.file.open('wb')
        # while rcv_data < int(length):
        #     data, addr = self.socket.receive()
        #     rcv_data += len(data)
        #     self.file.write(data)
        # self.file.close()

        #protocol = SelectiveRepeat.SelectiveRepeat(self.socket)
        protocol = StopAndWait.StopAndWait(self.socket)
        protocol.receive(self.file, int(length))
        self.file.close()
        self.socket.close()

    def close_socket(self):
        self.socket.close()
