from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

class ComputerData:
    def __init__(self, id, cpu_temp, gpu_temp, uptime, ram_usage):
        self.id = id
        self.cpu_temp = cpu_temp
        self.gpu_temp = gpu_temp
        self.uptime = uptime
        self.ram_usage = ram_usage
        self.timestamp = time.time()

computers_data = {}

@app.route('/performance', methods=['POST'])
def performance():
    data = request.get_json()
    computer_id = data.get('id', request.remote_addr)
    computers_data[computer_id] = ComputerData(
        id=computer_id,
        cpu_temp=data['CPUTemperature'],
        gpu_temp=data['GPUTemperature'],
        uptime=data['SystemUptime'],
        ram_usage=data['RAMUsage']
    )
    print(f"Received data from {computer_id}")
    return jsonify({"status": "success"}), 200

@app.route('/all_data', methods=['GET'])
def all_data():
    response_data = [
        {
            'id': comp.id,
            'cpu_temp': comp.cpu_temp,
            'gpu_temp': comp.gpu_temp,
            'uptime': comp.uptime,
            'ram_usage': comp.ram_usage,
            'timestamp': comp.timestamp
        }
        for comp in computers_data.values()
    ]
    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
