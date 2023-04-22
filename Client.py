import socket

import SelectiveRepeat
import StopAndWait
from Logging import Logging
from SocketUdp import SocketUdp
import File


class Client:
    def __init__(self, server_host, server_port):
        self.server_address = (server_host, server_port)
        self.socket = SocketUdp()
        self.address = None
        self.file = None
        self.protocol_message = None
        self.log = Logging()

    def send_operation(self, operation, fpath, fname):
        self.log.info('Enviamos operacion')
        self.file = File.File(fpath, fname)
        if operation == "u":
            self.protocol_message = operation + '#' + str(self.file.size()) + '#' + fname
        else:
            self.protocol_message = operation + '#' + fname
        encoded_message = str.encode(self.protocol_message)
        self.socket.sendto(encoded_message, self.server_address)

    def wait_confirmation(self):
        timeouts = 0
        self.log.info('Esperamos confirmacion')
        while timeouts < 5:
            self.log.info("Intento numero: " + str(timeouts + 1))
            self.socket.timeout(2)
            try:
                confirmation, new_address = self.socket.receive()
                self.log.info('Recibimos confirmacion')
                self.address = new_address
                return True
            except socket.timeout:
                timeouts += 1
                self.socket.sendto(self.protocol_message.encode(), self.server_address)

        return False

    def receive_length(self):
        timeouts = 0
        self.log.info('Esperamos longitud del archivo')
        while timeouts < 5:
            self.log.info("Intento numero: " + str(timeouts + 1))
            self.socket.timeout(2)
            try:
                length, new_address = self.socket.receive()
                self.log.info('Recibimos longitud')
                self.address = new_address
                return length
            except socket.timeout:
                timeouts += 1
                self.socket.sendto(self.protocol_message.encode(), self.server_address)

        return 0

    def send_confirmation(self):
        self.log.info('Enviamos confirmacion', self.address)
        self.socket.sendto('g'.encode(), self.address)

    def send_file(self, transport_protocol):
        self.log.info("Enviamos archivo")
        self.file.open("rb")
        if transport_protocol == "saw":
            protocol = StopAndWait.StopAndWait(self.socket)
        elif transport_protocol == "sr":
            protocol = SelectiveRepeat.SelectiveRepeat(self.socket)
        protocol.send(self.file, self.address)
        self.file.close()
        self.socket.close()

    def receive_file(self, length, transport_protocol):
        self.file.open('wb')
        if(transport_protocol == "saw"):
            protocol = StopAndWait.StopAndWait(self.socket)
        elif(transport_protocol == "sr"):
            protocol = SelectiveRepeat.SelectiveRepeat(self.socket)
        protocol.receive(self.file, int(length))
        self.file.close()
        self.socket.close()

    def close_socket(self):
        self.socket.close()
