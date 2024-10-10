import socket
import json

def save_record(record):
    with open('dns_records.json', 'w') as f:
        json.dump(record, f)

def load_record():
    try:
        with open('dns_records.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def handle_registration(data):
    record = dict(line.split('=') for line in data.split('\n') if '=' in line)
    save_record(record)
    return b"Registration successful"

def handle_query(data):
    query = dict(line.split('=') for line in data.split('\n') if '=' in line)
    record = load_record()
    if query.get('NAME') == record.get('NAME') and query.get('TYPE') == record.get('TYPE'):
        return f"TYPE={record['TYPE']}\nNAME={record['NAME']}\nVALUE={record['VALUE']}\nTTL={record['TTL']}\n".encode()
    return b"Not found"

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 53533))
    
    print("Authoritative Server is running...")
    
    while True:
        try:
            data, addr = server_socket.recvfrom(1024)
            data = data.decode()
            
            if all(key in data for key in ['TYPE=A', 'NAME=', 'VALUE=']):
                response = handle_registration(data)
            elif all(key in data for key in ['TYPE=A', 'NAME=']):
                response = handle_query(data)
            else:
                response = b"Invalid request"
            
            server_socket.sendto(response, addr)
        except Exception as e:
            print(f"Error handling request: {str(e)}")

if __name__ == "__main__":
    main()