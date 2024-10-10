from flask import Flask, request, jsonify
import socket
import requests

app = Flask(__name__)

HOSTNAME = "fibonacci.com"
IP = "172.18.0.2"
AS_IP = None
AS_PORT = None

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

@app.route('/register', methods=['PUT'])
def register():
    global AS_IP, AS_PORT
    data = request.json
    AS_IP = data['as_ip']
    AS_PORT = data['as_port']

    dns_reg = f"TYPE=A\nNAME={HOSTNAME}\nVALUE={IP}\nTTL=10\n"
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(dns_reg.encode(), (AS_IP, int(AS_PORT)))
    
    return "Registered successfully", 201

@app.route('/fibonacci')
def get_fibonacci():
    number = request.args.get('number')
    if not number or not number.isdigit():
        return "Bad Request: Invalid number", 400
    
    result = fibonacci(int(number))
    return jsonify({"fibonacci": result}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)