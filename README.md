# CPU Scheduling Calculator

so basically, this is a web app to calculate and visualize different cpu scheduling algorithms. i built it using plain HTML, CSS, and vanilla JS on the front end, and a Python Flask backend to do all the heavy lifting.

## Algorithms Included
It can handle the standard 6 algorithms discussed in OS class:
- First-Come, First-Serve (FCFS)
- Shortest Job First (SJF) - non-preemptive
- Shortest Remaining Time First (SRTF) - preemptive
- Priority (non-preemptive)
- Priority (preemptive)
- Round Robin (RR)

## How to Run
it's pretty simple to get running locally. you just need python installed.

1. clone the repo and go to the folder
2. install the dependencies (it's just flask):
   ```bash
   pip install -r requirements.txt
   ```
3. run the app:
   ```bash
   python app.py
   ```
4. open your browser and go to `http://127.0.0.1:5000`

## how it works
the frontend is a single `index.html` page styled with a custom dark-mode css file. when you add your processes and hit calculate, the Javascrip grabs the data and sends a POST request to the flask server. the Python backend runs the math based on the algorithm you picked, and sends back the gantt chart timeline and turnaround/waiting time metrics. then the JS just renders it nicely on the screen.

yeah, that's pretty much it
