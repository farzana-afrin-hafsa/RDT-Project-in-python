import socket
import time
from packet_utils import create_packet

def sender(server_ip, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)  # Timeout for retransmission

    data_to_send = ["Hello", "Reliable", "Data", "Transfer", "Protocol"]
    seq_num = 0

    for data in data_to_send:
        packet = create_packet(seq_num, data)
        while True:
            print(f"Sender: Sending packet: {packet}")
            sock.sendto(packet.encode(), (server_ip, server_port))

            try:
                # Wait for acknowledgment
                ack, _ = sock.recvfrom(1024)
                ack = ack.decode()

                if ack == f"ACK{seq_num}":
                    print(f"Sender: Received ACK{seq_num}")
                    seq_num = 1 - seq_num  # Toggle sequence number
                    break
                else:
                    print(f"Sender: Received unexpected ACK: {ack}. Resending...")
            except socket.timeout:
                print("Sender: Timeout occurred. Resending packet...")

    sock.close()

if __name__ == "__main__":
    sender("127.0.0.1", 12345)
