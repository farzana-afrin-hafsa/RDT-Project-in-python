import hashlib

# Function to calculate checksum
def calculate_checksum(data):
    return hashlib.md5(data.encode()).hexdigest()

# Function to create a packet with sequence number, data, and checksum
def create_packet(seq_num, data):
    checksum = calculate_checksum(data)
    return f"{seq_num}|{data}|{checksum}"

# Function to validate a received packet
def validate_packet(packet):
    try:
        seq_num, data, received_checksum = packet.split('|')
        calculated_checksum = calculate_checksum(data)
        return calculated_checksum == received_checksum, int(seq_num), data
    except ValueError:
        return False, None, None
