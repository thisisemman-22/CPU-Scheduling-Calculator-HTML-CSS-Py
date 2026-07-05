# CPU Scheduling Calculator

so basically, this is a web app to calculate and visualize different cpu scheduling algorithms. we built it using plain html, css, and vanilla javascript on the front end, and a python flask backend to do all the heavy math. no react, no complex build steps, just the basics.

## algorithms included
it can handle the standard 6 algorithms you'd see in an OS class:
- First-Come, First-Serve (FCFS)
- Shortest Job First (SJF) - non-preemptive
- Shortest Remaining Time First (SRTF) - preemptive
- Priority (non-preemptive)
- Priority (preemptive)
- Round Robin (RR)

## how to run it
it's pretty simple to get running locally. you just need python installed.

1. clone the repo and go to the folder
2. install the dependencies (it's just flask really):
   ```bash
   pip install -r requirements.txt
   ```
3. run the app:
   ```bash
   python app.py
   ```
4. open your browser and go to `http://127.0.0.1:5000`

## how it works
the frontend is a single `index.html` page styled with a custom dark-mode css file. when you add your processes and hit calculate, the javascript grabs the data and sends a POST request to the flask server. the python backend runs the math based on the algorithm you picked, and sends back the gantt chart timeline and turnaround/waiting time metrics. then the js just renders it nicely on the screen.

yeah, that's pretty much it!
