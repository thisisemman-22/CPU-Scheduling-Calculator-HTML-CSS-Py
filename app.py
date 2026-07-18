import threading
import sys
import os
import webview
from flask import Flask, request, jsonify, render_template
from algorithms import fcfs, sjf, srtf, priority_np, priority_p, round_robin

# For PyInstaller to find templates/static correctly when bundled
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    
    algorithm = data.get('algorithm', 'FCFS')
    time_quantum = int(data.get('timeQuantum', 2))
    processes = data.get('processes', [])
    
    if not processes:
        return jsonify({"gantt": [], "metrics": {}})
        
    if algorithm == 'FCFS':
        result = fcfs(processes)
    elif algorithm == 'SJF':
        result = sjf(processes)
    elif algorithm == 'SRTF':
        result = srtf(processes)
    elif algorithm == 'PriorityNP':
        result = priority_np(processes)
    elif algorithm == 'PriorityP':
        result = priority_p(processes)
    elif algorithm == 'RR':
        result = round_robin(processes, time_quantum)
    else:
        result = fcfs(processes)
        
    return jsonify(result)

def start_server():
    app.run(host='127.0.0.1', port=5000)

if __name__ == '__main__':
    # Start Flask server in a background thread
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()
    
    # Open PyWebView Desktop Window pointing to the local Flask server
    webview.create_window('CPU Scheduler', 'http://127.0.0.1:5000', width=1200, height=800)
    webview.start()
