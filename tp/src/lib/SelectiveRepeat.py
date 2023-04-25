import socket
import math
from lib.Logging import Logging


class SelectiveRepeat:
    CHUNK_SIZE = 1469
    SEQ_NUM_SIZE = 3

    def __init__(self, socket):
        self.socket = socket
        self.base = 0
        self.next_seq_num = 0
        self.unacked_packets = {}
        self.expected_seq_num = 0
        self.buffer = {}
        self.window_size = 0
        self.log = Logging()

    def __pack(self, seqnum, data: bytearray):
        return seqnum + data

    def __unpack(self, packet):
        seq_num = packet[: self.SEQ_NUM_SIZE]
        data = packet[self.SEQ_NUM_SIZE:]
        return seq_num, data

    def send(self, file, addr):
        len_packets = math.ceil(file.size() / self.CHUNK_SIZE)

        self.window_size = (len_packets / 2) - 1 if ((len_packets / 2) - 1 > 0) else 1

        while True:
            # Send packets up to window size
            while (
                self.next_seq_num < self.base + self.window_size
                and self.next_seq_num < len_packets
            ):
                packet = file.read(self.CHUNK_SIZE)
                seq_num = self.next_seq_num
                data = self.__pack(seq_num.to_bytes(3, byteorder="big"), packet)
                self.log.info("Enviamos paquete de {} bytes".format(len(packet)), addr)

                self.socket.sendto(data, addr)

                self.unacked_packets[seq_num] = packet
                self.next_seq_num += 1

            # Receive ACKs and update state
            if self.base < len_packets:
                self.socket.timeout(0.1)
                try:
                    ack, addr = self.socket.receive()
                    seq_num_receive, _ = self.__unpack(ack)

                    ack_num = int.from_bytes(seq_num_receive, "big")

                    del self.unacked_packets[ack_num]
                    self.base += 1

                except socket.timeout:
                    # Resend unacknowledged packets
                    for seq_num, packet in self.unacked_packets.items():
                        self.socket.timeout(None)
                        self.socket.sendto(
                            self.__pack(seq_num.to_bytes(3, byteorder="big"), packet),
                            addr,
                        )

            # Exit loop if all packets have been acknowledged
            if self.base == len_packets:
                self.log.info("Ultimo paquete transmitido")
                break

    def receive(self, file, buffsize):
        rcv_data = 0
        last_write = -1
        first_time = True
        self.socket.timeout(5)
        while True:
            try:
                # Receive packet
                packet, addr = self.socket.receive()
                first_time = False
                self.log.info("Recibimos paquete de {} bytes".format(len(packet)), addr)

                seq_num, data = self.__unpack(packet)
                seq_num_int = int.from_bytes(seq_num, "big")
                self.log.info(
                    "Numero de secuencia esperado {} y recibido {}".format(
                        self.expected_seq_num, seq_num_int
                    ),
                    addr,
                )

                # Send ACK for received packet
                ack = self.__pack(seq_num, b"")
                self.socket.sendto(ack, addr)

                # If the packet is the expected one, write its data to the file
                if seq_num_int == self.expected_seq_num:
                    # Write packet data to file
                    file.write(data)
                    self.expected_seq_num += 1
                    rcv_data += len(data)
                    last_write += 1

                    while rcv_data < buffsize:
                        try:
                            data = self.buffer[last_write + 1]
                            file.write(data)
                            del self.buffer[last_write + 1]
                            self.expected_seq_num += 1
                            rcv_data += len(data)
                            last_write += 1
                        except:
                            break
                else:
                    self.buffer[seq_num_int] = data
            except socket.timeout:
                if first_time:
                    break
                elif rcv_data < buffsize:
                    continue
                else:
                    break
        self.log.info("No obtuve paquete, finalizamos")
