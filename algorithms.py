def fcfs(processes):
    # First-Come, First-Serve runs jobs in arrival order and never preempts them.
    gantt = []
    metrics = {}
    
    # Sort by arrival time first so the earliest ready process runs first.
    sorted_processes = sorted(processes, key=lambda x: (x['at'], int(x['id'][1:])))
    
    # Simulated clock for the CPU timeline.
    current_time = 0
    
    for p in sorted_processes:
        # If the next process has not arrived yet, record an idle gap.
        if current_time < p['at']:
            gantt.append({"id": "Idle", "start": current_time, "end": p['at']})
            current_time = p['at']
            
        # The process starts immediately once the CPU reaches its arrival time.
        start_time = current_time
        completion_time = current_time + p['bt']
        
        # Store the execution block in the Gantt chart.
        gantt.append({"id": p['id'], "start": start_time, "end": completion_time})
        
        # Turnaround time is total time in the system.
        turnaround_time = completion_time - p['at']
        # Waiting time is everything except the time actually on the CPU.
        waiting_time = turnaround_time - p['bt']
        
        # Save the per-process metrics for the results table.
        metrics[p['id']] = {
            "id": p['id'],
            "at": p['at'],
            "bt": p['bt'],
            "priority": p['priority'],
            "st": start_time,
            "ct": completion_time,
            "tat": turnaround_time,
            "wt": waiting_time
        }
        
        current_time = completion_time
        
    return {"gantt": gantt, "metrics": metrics}


def sjf(processes):
    # Shortest Job First always picks the shortest available burst next.
    gantt = []
    metrics = {}
    
    # Work on a copy so the original input data stays untouched.
    remaining = [dict(p) for p in processes]
    # Simulated CPU clock.
    current_time = 0
    
    while len(remaining) > 0:
        # Only processes that have already arrived can be scheduled.
        available = [p for p in remaining if p['at'] <= current_time]
        
        if len(available) == 0:
            # If nothing is ready, jump forward to the next arrival.
            next_arrival = min([p['at'] for p in remaining])
            gantt.append({"id": "Idle", "start": current_time, "end": next_arrival})
            current_time = next_arrival
            continue
            
        # Choose the shortest job, using arrival time and ID as tie-breakers.
        available.sort(key=lambda x: (x['bt'], x['at'], int(x['id'][1:])))
        
        p = available[0]
        # Non-preemptive SJF runs the chosen job to completion.
        start_time = current_time
        completion_time = current_time + p['bt']
        
        # Add the full execution block to the chart.
        gantt.append({"id": p['id'], "start": start_time, "end": completion_time})
        
        turnaround_time = completion_time - p['at']
        waiting_time = turnaround_time - p['bt']
        
        # Save the metrics for the selected job.
        metrics[p['id']] = {
            "id": p['id'],
            "at": p['at'],
            "bt": p['bt'],
            "priority": p['priority'],
            "st": start_time,
            "ct": completion_time,
            "tat": turnaround_time,
            "wt": waiting_time
        }
        
        current_time = completion_time
        remaining = [r for r in remaining if r['id'] != p['id']]
        
    return {"gantt": gantt, "metrics": metrics}


def srtf(processes):
    # Shortest Remaining Time First is the preemptive version of SJF.
    gantt = []
    metrics = {}
    
    # Add scheduler-only fields to a copy of each process.
    remaining_processes = []
    for p in processes:
        new_p = dict(p)
        new_p['rt'] = p['bt']
        new_p['st'] = -1
        remaining_processes.append(new_p)
        
    # Track the state of the simulated CPU.
    current_time = 0
    completed = 0
    prev_id = None
    block_start = 0
    
    while completed < len(processes):
        # Find every process that has arrived and still has work left.
        available = [p for p in remaining_processes if p['at'] <= current_time and p['rt'] > 0]
        
        if len(available) == 0:
            # Close the active block and fast-forward to the next arrival.
            if prev_id is not None:
                gantt.append({"id": prev_id, "start": block_start, "end": current_time})
                prev_id = None
                
            future_arrivals = [p['at'] for p in remaining_processes if p['rt'] > 0]
            next_arrival = min(future_arrivals)
            
            # Record idle time so the chart stays continuous.
            if prev_id != "Idle":
                block_start = current_time
                prev_id = "Idle"
                
            current_time = next_arrival
            continue
            
        # Pick the process with the smallest remaining burst time.
        available.sort(key=lambda x: (x['rt'], x['at'], int(x['id'][1:])))
        
        p = available[0]
        
        # When the active process changes, close the previous block first.
        if prev_id != p['id']:
            if prev_id is not None:
                gantt.append({"id": prev_id, "start": block_start, "end": current_time})
            block_start = current_time
            prev_id = p['id']
            
        # Save the first time this process actually receives CPU time.
        if p['st'] == -1:
            p['st'] = current_time
            
        # Run only until the next arrival if another process might preempt soon.
        future_arrivals = [r['at'] for r in remaining_processes if r['at'] > current_time and r['rt'] > 0]
        
        if len(future_arrivals) > 0:
            next_arrival = min(future_arrivals)
            time_to_run = min(p['rt'], next_arrival - current_time)
        else:
            time_to_run = p['rt']
            
        # Advance time and reduce the remaining work for the active process.
        p['rt'] -= time_to_run
        current_time += time_to_run
        
        # Once the process finishes, calculate and store its metrics.
        if p['rt'] == 0:
            completed += 1
            completion_time = current_time
            turnaround_time = completion_time - p['at']
            waiting_time = turnaround_time - p['bt']
            
            metrics[p['id']] = {
                "id": p['id'],
                "at": p['at'],
                "bt": p['bt'],
                "priority": p['priority'],
                "st": p['st'],
                "ct": completion_time,
                "tat": turnaround_time,
                "wt": waiting_time
            }
            
    if prev_id is not None:
        gantt.append({"id": prev_id, "start": block_start, "end": current_time})
        
    # Keep every Round Robin slice separate so the chart shows each quantum.
    return {"gantt": gantt, "metrics": metrics}


def priority_np(processes):
    # Non-preemptive priority scheduling picks the highest priority job available.
    gantt = []
    metrics = {}
    
    # Copy the data so the input list is not modified.
    remaining = [dict(p) for p in processes]
    # Simulated CPU clock.
    current_time = 0
    
    while len(remaining) > 0:
        # Only processes that have arrived can compete for the CPU.
        available = [p for p in remaining if p['at'] <= current_time]
        
        if len(available) == 0:
            # No process is ready, so move to the next arrival.
            next_arrival = min([p['at'] for p in remaining])
            gantt.append({"id": "Idle", "start": current_time, "end": next_arrival})
            current_time = next_arrival
            continue
            
        # Lower priority numbers mean higher priority in this project.
        available.sort(key=lambda x: (x['priority'], x['at'], int(x['id'][1:])))
        
        p = available[0]
        # Non-preemptive priority runs the selected process to completion.
        start_time = current_time
        completion_time = current_time + p['bt']
        
        # Record the execution block for the chosen process.
        gantt.append({"id": p['id'], "start": start_time, "end": completion_time})
        
        turnaround_time = completion_time - p['at']
        waiting_time = turnaround_time - p['bt']
        
        # Save the metrics for display in the frontend.
        metrics[p['id']] = {
            "id": p['id'],
            "at": p['at'],
            "bt": p['bt'],
            "priority": p['priority'],
            "st": start_time,
            "ct": completion_time,
            "tat": turnaround_time,
            "wt": waiting_time
        }
        
        current_time = completion_time
        remaining = [r for r in remaining if r['id'] != p['id']]
        
    return {"gantt": gantt, "metrics": metrics}


def priority_p(processes):
    # Preemptive priority scheduling can switch when a higher priority job arrives.
    gantt = []
    metrics = {}
    
    # Add scheduler-only fields to a copy of each process.
    remaining_processes = []
    for p in processes:
        new_p = dict(p)
        new_p['rt'] = p['bt']
        new_p['st'] = -1
        remaining_processes.append(new_p)
        
    # Track the simulated CPU state.
    current_time = 0
    completed = 0
    prev_id = None
    block_start = 0
    
    while completed < len(processes):
        # Find all processes that can run right now.
        available = [p for p in remaining_processes if p['at'] <= current_time and p['rt'] > 0]
        
        if len(available) == 0:
            # Close the current block and jump to the next arrival.
            if prev_id is not None:
                gantt.append({"id": prev_id, "start": block_start, "end": current_time})
                prev_id = None
                
            future_arrivals = [p['at'] for p in remaining_processes if p['rt'] > 0]
            next_arrival = min(future_arrivals)
            
            # Record idle time while waiting for the next process.
            if prev_id != "Idle":
                block_start = current_time
                prev_id = "Idle"
                
            current_time = next_arrival
            continue
            
        # Lower priority values win, with arrival time and ID as tie-breakers.
        available.sort(key=lambda x: (x['priority'], x['at'], int(x['id'][1:])))
        
        p = available[0]
        
        # If a new process is selected, close the previous gantt block.
        if prev_id != p['id']:
            if prev_id is not None:
                gantt.append({"id": prev_id, "start": block_start, "end": current_time})
            block_start = current_time
            prev_id = p['id']
            
        # Save the first time this process gets CPU time.
        if p['st'] == -1:
            p['st'] = current_time
            
        # Only run until the next competing arrival or until the process finishes.
        future_arrivals = [r['at'] for r in remaining_processes if r['at'] > current_time and r['rt'] > 0]
        
        if len(future_arrivals) > 0:
            next_arrival = min(future_arrivals)
            time_to_run = min(p['rt'], next_arrival - current_time)
        else:
            time_to_run = p['rt']
            
        # Advance the clock and reduce the process's remaining work.
        p['rt'] -= time_to_run
        current_time += time_to_run
        
        # Save metrics when the process finishes.
        if p['rt'] == 0:
            completed += 1
            completion_time = current_time
            turnaround_time = completion_time - p['at']
            waiting_time = turnaround_time - p['bt']
            
            metrics[p['id']] = {
                "id": p['id'],
                "at": p['at'],
                "bt": p['bt'],
                "priority": p['priority'],
                "st": p['st'],
                "ct": completion_time,
                "tat": turnaround_time,
                "wt": waiting_time
            }
            
    if prev_id is not None:
        gantt.append({"id": prev_id, "start": block_start, "end": current_time})
        
    # Merge adjacent blocks with the same ID so the chart stays readable.
    final_gantt = []
    for b in gantt:
        if len(final_gantt) > 0 and final_gantt[-1]['id'] == b['id']:
            final_gantt[-1]['end'] = b['end']
        else:
            final_gantt.append(b)
            
    return {"gantt": final_gantt, "metrics": metrics}


def round_robin(processes, time_quantum):
    # Round Robin gives each process a fixed time slice called a quantum.
    if time_quantum <= 0:
        raise ValueError("time_quantum must be greater than zero")

    gantt = []
    metrics = {}
    
    remaining_processes = []
    for p in processes:
        new_p = dict(p)
        new_p['rt'] = p['bt']
        new_p['st'] = -1
        remaining_processes.append(new_p)
        
    # Sort by arrival time first so queue order is predictable.
    remaining_processes.sort(key=lambda x: (x['at'], int(x['id'][1:])))
    
    current_time = 0
    queue = []
    completed = 0
    i = 0 
    
    # Load any processes that have already arrived at time zero.
    while i < len(remaining_processes) and remaining_processes[i]['at'] <= current_time:
        queue.append(remaining_processes[i])
        i += 1
        
    while completed < len(processes):
        if len(queue) == 0:
            # If nothing is ready, jump to the next arrival and record idle time.
            next_arrival = remaining_processes[i]['at']
            if current_time < next_arrival:
                gantt.append({"id": "Idle", "start": current_time, "end": next_arrival})
            current_time = next_arrival
            
            # Add every process that has now arrived.
            while i < len(remaining_processes) and remaining_processes[i]['at'] <= current_time:
                queue.append(remaining_processes[i])
                i += 1
            continue
            
        p = queue.pop(0)

        # Save the first time this process receives CPU time.
        if p['st'] == -1:
            p['st'] = current_time

        # Run for one quantum or until the process finishes, whichever comes first.
        slice_start = current_time
        time_to_run = min(p['rt'], time_quantum)
        p['rt'] -= time_to_run
        current_time += time_to_run
        # Each quantum is kept as its own block so the split is visible.
        gantt.append({"id": p['id'], "start": slice_start, "end": current_time})
        
        # Add processes that arrived while this slice was running.
        while i < len(remaining_processes) and remaining_processes[i]['at'] <= current_time:
            queue.append(remaining_processes[i])
            i += 1
            
        if p['rt'] == 0:
            # Once a process finishes, calculate and store its metrics.
            completed += 1
            completion_time = current_time
            turnaround_time = completion_time - p['at']
            waiting_time = turnaround_time - p['bt']
            
            metrics[p['id']] = {
                "id": p['id'],
                "at": p['at'],
                "bt": p['bt'],
                "priority": p['priority'],
                "st": p['st'],
                "ct": completion_time,
                "tat": turnaround_time,
                "wt": waiting_time
            }
        else:
            queue.append(p) 

    return {"gantt": gantt, "metrics": metrics}
