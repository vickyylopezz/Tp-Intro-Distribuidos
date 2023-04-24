import socket

from Logging import Logging
from Timer import Timer
from time import perf_counter as now


def toggle(seq_number):
    if seq_number == b"0":
        return b"1"
    return b"0"


class StopAndWait:
    SEQ_NUM_SIZE = 1
    MAX_TIMEOUTS = 6
    CHUNK_SIZE = 1471

    def __init__(self, socket):
        self.sender_seqnum = b"0"
        self.receiver_seqnum = b"0"
        self.socket = socket
        self.timer = Timer()
        self.log = Logging()

    def __pack(self, seqnum, data: bytearray):
        return seqnum + data

    def __unpack(self, packet):
        seq_num = packet[: self.SEQ_NUM_SIZE]
        data = packet[self.SEQ_NUM_SIZE:]
        return seq_num, data

    def _send_a_packet(self, data, addr, last_send):
        pkt = self.__pack(self.sender_seqnum, data)
        self.log.info("Enviamos paquete de {} bytes".format(len(pkt)), addr)
        self.socket.sendto(pkt, addr)
        start = now()
        acknowledged = False
        timeouts = 0
        if last_send:
            self.log.info("Ultimo paquete")
        while not acknowledged:
            try:
                timeout = self.timer.getTimeout() - (now() - start)
                self.socket.timeout(timeout)
                pkt_received, _ = self.socket.receive()
                seq_num_received, _ = self.__unpack(pkt_received)
                if seq_num_received == self.sender_seqnum:
                    self.timer.calculateTimeout(now() - start)
                    self.socket.timeout(None)
                    self.sender_seqnum = toggle(self.sender_seqnum)
                    acknowledged = True

            except socket.timeout:
                if last_send:
                    timeouts += 1
                self.timer.timeout()
                self.socket.sendto(pkt, addr)
                start = now()

            if last_send and timeouts >= self.MAX_TIMEOUTS:
                self.sender_seqnum = toggle(self.sender_seqnum)
                self.socket.timeout(None)
                break

    def send(self, file, addr):
        while True:
            last_send = False
            chunk = file.read(self.CHUNK_SIZE)
            if not chunk:
                break
            if len(chunk) < self.CHUNK_SIZE:
                last_send = True
            self._send_a_packet(chunk, addr, last_send)

    def _recv(self, file_size, first_time):
        correct_seq_numb = False
        if first_time:
            self.socket.timeout(10)
        else:
            self.socket.timeout(None)

        try:
            while not correct_seq_numb:
                pkt_received, source = self.socket.receive()
                self.log.info(
                    "Recibimos paquete de {} bytes".format(len(pkt_received)), source
                )
                seq_num_received, data_received = self.__unpack(pkt_received)
                self.log.info(
                    "Numero de secuencia esperado {} y recibido {}".format(
                        self.receiver_seqnum, seq_num_received
                    ),
                    source,
                )
                if seq_num_received == self.receiver_seqnum:
                    pkt = self.__pack(self.receiver_seqnum, b"")
                    self.socket.sendto(pkt, source)
                    self.receiver_seqnum = toggle(self.receiver_seqnum)
                    correct_seq_numb = True
                else:
                    pkt = self.__pack(toggle(self.receiver_seqnum), b"")
                    self.socket.sendto(pkt, source)

            return data_received

        except:
            return 0

    def receive(self, file, file_size):
        rcv_data = 0
        first_time = True
        while rcv_data < file_size:
            data = self._recv(file_size, first_time)
            if data == 0:
                self.socket.close()
                self.log.info("No obtuve paquete, finalizamos")
                exit(1)
            rcv_data += len(data)
            file.write(data)
            first_time = False
