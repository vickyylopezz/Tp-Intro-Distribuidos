import socket

from Logging import Logging
from Timer import Timer
from time import perf_counter as now


def toggle(seq_number):
    if seq_number == b'0':
        return b'1'
    return b'0'


class StopAndWait:
    SEQ_NUM_SIZE = 1
    MAX_TIMEOUTS = 6
    CHUNK_SIZE = 1471

    def __init__(self, socket):
        self.sender_seqnum = b'0'
        self.receiver_seqnum = b'0'
        self.socket = socket
        self.timer = Timer()

    def __pack(self, seqnum, data: bytearray):
        return seqnum + data

    def __unpack(self, packet):
        seq_num = packet[:self.SEQ_NUM_SIZE]
        data = packet[self.SEQ_NUM_SIZE:]
        return seq_num, data

    def _send_a_packet(self, data, addr, last_send):
        log = Logging()

        pkt = self.__pack(self.sender_seqnum, data)
        # sent = self.socket.sendto(pkt, addr)
        self.socket.sendto(pkt, addr)
        start = now()
        acknowledged = False
        timeouts = 0
        if last_send:
            log.log("Ultimo paquete")
        while not acknowledged:
            try:
                timeout = self.timer.getTimeout() - (now() - start)
                self.socket.timeout(timeout)
                # print(timeout)
                pkt_received, _ = self.socket.receive()  # revisar, puede ser que le tengamos que pasar el tamanio del mensaje esperado
                # puede ser que sirva la direccion que devuelve por el multithreading
                seq_num_received, _ = self.__unpack(pkt_received)

                # print("waiting:")
                # print(self.sender_seqnum)
                # print("received:")
                # print(seq_num_received)
                if seq_num_received == self.sender_seqnum:
                    self.timer.calculateTimeout(now() - start)
                    self.socket.timeout(None)
                    self.sender_seqnum = toggle(self.sender_seqnum)
                    acknowledged = True

            except socket.timeout:
                if last_send:
                    timeouts += 1
                # print("timeout")
                self.timer.timeout()
                # sent = self.socket.sendto(pkt, addr)
                self.socket.sendto(pkt, addr)
                start = now()

            if last_send and timeouts >= self.MAX_TIMEOUTS:
                self.sender_seqnum = toggle(self.sender_seqnum)
                self.socket.timeout(None)
                break

        # return sent

    def send(self, file, addr):
        # _data = bytearray(data)
        # sent = 0

        # for i in range(0, len(_data), self.MAX_DATAGRAM_SIZE):
        #     last_send = False

        #     if i + self.MAX_DATAGRAM_SIZE > len(_data):
        #         last_send = True

        #     sent += self._send_a_packet(
        #         _data[i:min(i + self.MAX_DATAGRAM_SIZE, len(_data))],
        #         host,
        #         port,
        #         last_send
        #     )

        # self.socket.settimeout(None)
        # return sent
        while True:
            last_send = False
            chunk = file.read(self.CHUNK_SIZE)
            if not chunk:
                break
            if len(chunk) < self.CHUNK_SIZE:
                last_send = True
            self._send_a_packet(chunk, addr, last_send)

    def _recv(self, buffsize, first_time):
        correct_seq_numb = False
        # print("-----chunks-----")
        # print(buffsize)
        # podriamos dejar el timeout para todos los casos, no?
        # si el cliente muere esperamos unos segundos y salimos
        # sino vamos a quedar esperando para siempre. Creo que es innecesario el first_time
        if first_time:
            self.socket.timeout(10)
        else:
            self.socket.timeout(None)

        try:
            while not correct_seq_numb:
                # pkt_received, source = self.socket.recvfrom(
                #     buffsize + self.SEQ_NUM_SIZE)
                pkt_received, source = self.socket.receive()
                seq_num_received, data_received = self.__unpack(pkt_received)

                # print("pkt:")
                # print(pkt_received)
                # print("waiting:")
                # print(self.receiver_seqnum)
                # print("seq num received:")
                # print(seq_num_received)
                # print(data_received)
                if seq_num_received == self.receiver_seqnum:
                    pkt = self.__pack(self.receiver_seqnum, b'')
                    self.socket.sendto(pkt, source)
                    self.receiver_seqnum = toggle(self.receiver_seqnum)
                    correct_seq_numb = True
                else:
                    pkt = self.__pack(toggle(self.receiver_seqnum), b'')
                    self.socket.sendto(pkt, source)

            return data_received

        except:
            return 0
        # return data_received, source

    def receive(self, file, buffsize):
        # print("quiero recibir estos bytes:")
        # print(buffsize)
        # data = []
        # for i in range(0, buffsize, self.MAX_DATAGRAM_SIZE):
        #     print("-------Iteracion numero-------")
        #     print(i)
        #     d, s = self._recv(min(self.MAX_DATAGRAM_SIZE, buffsize - i))
        #     data.append(d)
        #
        # data = b''.join(data)
        # print("received")
        # print(data)
        # return data, s
        rcv_data = 0
        first_time = True
        while rcv_data < buffsize:
            # data, addr = self._recv()
            data = self._recv(buffsize, first_time)
            if data == 0:
                self.socket.close()
                print("No obtuve datos del otro lado, desconectando")
                exit(1)
            rcv_data += len(data)
            file.write(data)
            first_time = False
