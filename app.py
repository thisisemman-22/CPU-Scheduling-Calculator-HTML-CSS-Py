from flask import Flask, request, jsonify, render_template
from algorithms import fcfs, sjf, srtf, priority_np, priority_p, round_robin

app = Flask(__name__)

@app.route('/')
def index():
    # Serve the main HTML page
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
