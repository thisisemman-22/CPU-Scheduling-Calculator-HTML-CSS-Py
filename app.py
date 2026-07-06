from flask import Flask, request, jsonify, render_template
from algorithms import fcfs, sjf, srtf, priority_np, priority_p, round_robin

# Flask application object that serves both the UI and the calculation endpoint.
app = Flask(__name__)

@app.route('/')
def index():
    # Return the main HTML page for the scheduler UI.
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Parse the JSON payload sent by the browser.
    data = request.get_json()
    
    # Default to FCFS if no algorithm name is supplied.
    algorithm = data.get('algorithm', 'FCFS')
    # Round Robin needs a positive quantum so it does not get stuck.
    try:
        time_quantum = int(data.get('timeQuantum', 2))
    except (TypeError, ValueError):
        return jsonify({"error": "Quantum must be a positive whole number."}), 400

    if time_quantum <= 0:
        return jsonify({"error": "Quantum must be greater than zero."}), 400

    # Pull the process list out of the request body.
    processes = data.get('processes', [])
    
    # If there is nothing to calculate, return an empty response shape.
    if not processes:
        return jsonify({"gantt": [], "metrics": {}})
        
    # Choose the matching scheduling algorithm.
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
        
    # Send the finished gantt chart and metrics back to the frontend.
    return jsonify(result)

if __name__ == '__main__':
    # Run the Flask development server when this file is executed directly.
    app.run(debug=True, port=5000)
