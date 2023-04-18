import socket

class SelectiveRepeat:

    WINDOW_SIZE = 4
    TIMEOUT = 2
    CHUNK_SIZE = 1471
    SEQ_NUM_SIZE = 2

    def __init__(self, socket):
        self.socket = socket
        self.base = 0
        self.next_seq_num = 0
        self.unacked_packets = {}
        self.expected_seq_num = 0
        self.buffer = {}
    
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
            print(len(packets))
            packets.append(chunk)
            if not chunk:
                break
        
        while True:
            # Send packets up to window size
            while self.next_seq_num < self.base + self.WINDOW_SIZE and self.next_seq_num < len(packets):
                print(packets)
                print(self.next_seq_num)
                packet = packets[self.next_seq_num]
                seq_num = self.next_seq_num
                self.socket.sendto(self.__pack(seq_num.to_bytes(2, byteorder="big"), packet), addr)
                self.unacked_packets[seq_num] = packet
                self.next_seq_num += 1

            # Receive ACKs and update state
            #self.socket.timeout(TIMEOUT)
            try:
                ack, addr = self.socket.receive()
                print("recibi ack")
                seq_num_receive, _ = self.__unpack(ack)
                print(seq_num_receive)
                ack_num = int.from_bytes(seq_num_receive, "big")
                if ack_num >= self.base:
                    # Update base and remove acknowledged packets from unacked_packets
                    self.base = ack_num + 1
                    for seq_num in range(self.base):
                        if seq_num in self.unacked_packets:
                            del self.unacked_packets[seq_num]
            except socket.timeout:
                # Resend unacknowledged packets
                for seq_num, packet in self.unacked_packets.items():
                    self.socket.sendto(self.__pack(seq_num.to_bytes(2, byteorder="big"), packet), addr)

            # Exit loop if all packets have been acknowledged
            if self.base == len(packets):
                break

    def receive(self, file, buffsize):
        file.write(b'hola2')
        while True:
            # Receive packet
            packet, addr = self.socket.receive()
            seq_num, data = self.__unpack(packet)
            seq_num_int = int.from_bytes(seq_num, "big")
            #seq_num = self.expected_seq_num
            print("recibi paquete: ", packet)
                
            # Send ACK for received packet
            ack = self.__pack(seq_num, data)
            self.socket.sendto(ack, addr)
            print("mande ack")


            # If the packet is the expected one, write its data to the file
            if  seq_num_int == self.expected_seq_num:
                # Write packet data to file
                write = file.write(data)
                print("escribi archivo",file, "con: ", data, write)
                self.expected_seq_num += 1
                
                print("Buffer:", self.buffer)
                print("expected seq num:", self.expected_seq_num)
                print(self.expected_seq_num in self.buffer)
                
                # Write any consecutive packets that were received out of order
                while self.expected_seq_num in self.buffer:
                    print("expected seq num:", self.expected_seq_num)
                    file.write(self.buffer[self.expected_seq_num])
                    del self.buffer[self.expected_seq_num]
                    self.expected_seq_num += 1
            else:
                self.buffer[seq_num] = data