from flask import Flask, request, jsonify
import requests
import socket

app = Flask(__name__)

def dns_query(hostname, as_ip, as_port):
    query = f"TYPE=A\nNAME={hostname}\n"
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(5)
        sock.sendto(query.encode(), (as_ip, int(as_port)))
        response, _ = sock.recvfrom(1024)
    return dict(line.split('=') for line in response.decode().split('\n') if '=' in line)

@app.route('/fibonacci')
def fibonacci():
    params = request.args
    required = ['hostname', 'fs_port', 'number', 'as_ip', 'as_port']
    if not all(param in params for param in required):
        return "Bad Request: Missing parameters", 400

    try:
        dns_result = dns_query(params['hostname'], params['as_ip'], params['as_port'])
        if 'VALUE' not in dns_result:
            return "Error: Could not resolve hostname", 404
        
        fs_ip = dns_result['VALUE']
        fs_url = f"http://{fs_ip}:{params['fs_port']}/fibonacci?number={params['number']}"
        response = requests.get(fs_url, timeout=5)
        
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return f"Error from Fibonacci Server: {response.text}", response.status_code

    except requests.exceptions.RequestException as e:
        return "Error: Could not connect to Fibonacci Server", 503
    except socket.timeout:
        return "Error: DNS query timed out", 504
    except Exception as e:
        return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)