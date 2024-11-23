import socket
import random
from packet_utils import validate_packet

def receiver(bind_ip, bind_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((bind_ip, bind_port))

    expected_seq_num = 0

    while True:
        packet, addr = sock.recvfrom(1024)
        packet = packet.decode()
        print(f"Receiver: Received packet: {packet}")

        # Simulate random packet loss
        if random.random() < 0.2:
            print("Receiver: Simulating packet loss or corruption.")
            continue

        valid, seq_num, data = validate_packet(packet)
        if valid and seq_num == expected_seq_num:
            print(f"Receiver: Valid packet. Sending ACK{seq_num}")
            sock.sendto(f"ACK{seq_num}".encode(), addr)
            expected_seq_num = 1 - expected_seq_num  # Toggle expected sequence number
        else:
            print("Receiver: Invalid packet or unexpected sequence number. Sending NAK.")
            sock.sendto(f"NAK{expected_seq_num}".encode(), addr)

if __name__ == "__main__":
    receiver("127.0.0.1", 12345)
