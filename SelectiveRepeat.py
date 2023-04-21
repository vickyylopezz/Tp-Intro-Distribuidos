import socket

class SelectiveRepeat:

    # WINDOW_SIZE = 4
    TIMEOUT = 2
    CHUNK_SIZE = 1470
    SEQ_NUM_SIZE = 2

    def __init__(self, socket):
        self.socket = socket
        self.base = 0
        self.next_seq_num = 0
        self.unacked_packets = {}
        self.expected_seq_num = 0
        self.buffer = {}
        self.window_size = 0
    
    def __pack(self, seqnum, data: bytearray):
        return seqnum + data
    
    def __unpack(self, packet):
        seq_num = packet[:self.SEQ_NUM_SIZE]
        data = packet[self.SEQ_NUM_SIZE:]
        return seq_num, data
    
    def send(self, file, addr):
        packets = []

        # Send packets to server
        while True:
            
            chunk = file.read(self.CHUNK_SIZE)
            if not chunk:
                break
            packets.append(chunk)

        self.window_size = (len(packets) / 2) - 1 if ((len(packets) / 2) - 1 > 0) else 1

        while True:

            # Send packets up to window size
            while self.next_seq_num < self.base + self.window_size and self.next_seq_num < len(packets):
                packet = packets[self.next_seq_num]
                seq_num = self.next_seq_num
                data = self.__pack(seq_num.to_bytes(2, byteorder="big"), packet)
                self.socket.sendto(data, addr)
                print("Envie paquete:", seq_num)
                self.unacked_packets[seq_num] = packet
                self.next_seq_num += 1
            
            # Receive ACKs and update state
            self.socket.timeout(self.TIMEOUT)
            if(self.base < len(packets)):
                try:
                    ack, addr = self.socket.receive()
                    seq_num_receive, _ = self.__unpack(ack)
                    ack_num = int.from_bytes(seq_num_receive, "big")
                    print("Recibi ack de:", ack_num, "y base:", self.base)
                    del self.unacked_packets[ack_num]
                    self.base += 1
                    print("Elimine ack de:", ack_num)
                    #if ack_num == self.base:
                    #    aux = self.base + 1
                    #    while aux not in self.unacked_packets and aux < len(packets):
                    #        aux = aux +1
                    #    self.base = aux

                    #if ack_num > self.base:
                        # Update base and remove acknowledged packets from unacked_packets
                        #if ack_num in self.unacked_packets:
                        #    print("Elimine ack de:", ack_num)
                        #    del self.unacked_packets[ack_num]
                except socket.timeout:
                    # Resend unacknowledged packets
                    for seq_num, packet in self.unacked_packets.items():
                        print("Reenvie paquete:", seq_num)
                        self.socket.sendto(self.__pack(seq_num.to_bytes(2, byteorder="big"), packet), addr)

            # Exit loop if all packets have been acknowledged
            if self.base == len(packets):
                print("entre if con len packets:", len(packets))
                break


    def receive(self, file, buffsize):
        rcv_data = 0
        last_write = -1
        print(buffsize)
        self.socket.timeout(5)
        while True:
        #while rcv_data < buffsize:
            try:
                print(rcv_data)
                # Receive packet
                packet, addr = self.socket.receive()
                seq_num, data = self.__unpack(packet)
                seq_num_int = int.from_bytes(seq_num, "big")
                print("Recibi paquete numero:" ,seq_num_int, "y esperaba: ", self.expected_seq_num)
                print("Ultimo escribi:", last_write)
                #seq_num = self.expected_seq_num
                
                # Send ACK for received packet
                ack = self.__pack(seq_num, b'')
                self.socket.sendto(ack, addr)
                #print("mande ack")

                # If the packet is the expected one, write its data to the file
                if  seq_num_int == self.expected_seq_num:
                    
                    # Write any consecutive packets that were received out of order
                    #while self.expected_seq_num in self.buffer:
                    # Write packet data to file
                    file.write(data)
                    self.expected_seq_num += 1
                    rcv_data += len(data)
                    last_write += 1
                    #print("Buffer:", self.buffer)
                    #print("expected seq num:", self.expected_seq_num)

                    print("last write:", last_write, "and expected:", self.expected_seq_num, "and i:", last_write+1)
                    print(rcv_data)
                    while rcv_data < buffsize:
                        try: 
                            data = self.buffer[last_write+1]
                            print("Escribi:", self.expected_seq_num, last_write+1)
                            #print("expected seq num:", self.expected_seq_num)
                            file.write(data)
                            del self.buffer[last_write+1]
                            self.expected_seq_num += 1
                            rcv_data += len(data)
                            last_write += 1
                            print("las write:", last_write, "expected:", self.expected_seq_num)
                        except:
                            break
                else:
                    print("Escribi paquete:", seq_num_int, "en el buffer")
                    self.buffer[seq_num_int] = data
            except socket.timeout:
                break
        print("Termine")

