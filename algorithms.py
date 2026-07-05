def fcfs(processes):
    gantt = []
    metrics = {}
    
    # Sort processes by Arrival Time (at), then by Process ID number
    sorted_processes = sorted(processes, key=lambda x: (x['at'], int(x['id'][1:])))
    
    current_time = 0
    
    for p in sorted_processes:
        if current_time < p['at']:
            gantt.append({"id": "Idle", "start": current_time, "end": p['at']})
            current_time = p['at']
            
        start_time = current_time
        completion_time = current_time + p['bt']
        
        gantt.append({"id": p['id'], "start": start_time, "end": completion_time})
        
        turnaround_time = completion_time - p['at']
        waiting_time = turnaround_time - p['bt']
        
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
    gantt = []
    metrics = {}
    
    remaining = [dict(p) for p in processes]
    current_time = 0
    
    while len(remaining) > 0:
        available = [p for p in remaining if p['at'] <= current_time]
        
        if len(available) == 0:
            next_arrival = min([p['at'] for p in remaining])
            gantt.append({"id": "Idle", "start": current_time, "end": next_arrival})
            current_time = next_arrival
            continue
            
        # Sort by Burst Time, then Arrival Time, then ID
        available.sort(key=lambda x: (x['bt'], x['at'], int(x['id'][1:])))
        
        p = available[0]
        start_time = current_time
        completion_time = current_time + p['bt']
        
        gantt.append({"id": p['id'], "start": start_time, "end": completion_time})
        
        turnaround_time = completion_time - p['at']
        waiting_time = turnaround_time - p['bt']
        
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
    gantt = []
    metrics = {}
    
    remaining_processes = []
    for p in processes:
        new_p = dict(p)
        new_p['rt'] = p['bt']  # Remaining Time
        new_p['st'] = -1       # Start Time
        remaining_processes.append(new_p)
        
    current_time = 0
    completed = 0
    prev_id = None
    block_start = 0
    
    while completed < len(processes):
        available = [p for p in remaining_processes if p['at'] <= current_time and p['rt'] > 0]
        
        if len(available) == 0:
            if prev_id is not None:
                gantt.append({"id": prev_id, "start": block_start, "end": current_time})
                prev_id = None
                
            future_arrivals = [p['at'] for p in remaining_processes if p['rt'] > 0]
            next_arrival = min(future_arrivals)
            
            if prev_id != "Idle":
                block_start = current_time
                prev_id = "Idle"
                
            current_time = next_arrival
            continue
            
        # Sort by remaining time, then arrival time, then ID
        available.sort(key=lambda x: (x['rt'], x['at'], int(x['id'][1:])))
        
        p = available[0]
        
        if prev_id != p['id']:
            if prev_id is not None:
                gantt.append({"id": prev_id, "start": block_start, "end": current_time})
            block_start = current_time
            prev_id = p['id']
            
        if p['st'] == -1:
            p['st'] = current_time
            
        # Fast forward logic
        future_arrivals = [r['at'] for r in remaining_processes if r['at'] > current_time and r['rt'] > 0]
        
        if len(future_arrivals) > 0:
            next_arrival = min(future_arrivals)
            time_to_run = min(p['rt'], next_arrival - current_time)
        else:
            time_to_run = p['rt']
            
        p['rt'] -= time_to_run
        current_time += time_to_run
        
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
        
    final_gantt = []
    for b in gantt:
        if len(final_gantt) > 0 and final_gantt[-1]['id'] == b['id']:
            final_gantt[-1]['end'] = b['end']
        else:
            final_gantt.append(b)
            
    return {"gantt": final_gantt, "metrics": metrics}


def priority_np(processes):
    gantt = []
    metrics = {}
    
    remaining = [dict(p) for p in processes]
    current_time = 0
    
    while len(remaining) > 0:
        available = [p for p in remaining if p['at'] <= current_time]
        
        if len(available) == 0:
            next_arrival = min([p['at'] for p in remaining])
            gantt.append({"id": "Idle", "start": current_time, "end": next_arrival})
            current_time = next_arrival
            continue
            
        # Sort by Priority (lower is better), then Arrival Time, then ID
        available.sort(key=lambda x: (x['priority'], x['at'], int(x['id'][1:])))
        
        p = available[0]
        start_time = current_time
        completion_time = current_time + p['bt']
        
        gantt.append({"id": p['id'], "start": start_time, "end": completion_time})
        
        turnaround_time = completion_time - p['at']
        waiting_time = turnaround_time - p['bt']
        
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
    gantt = []
    metrics = {}
    
    remaining_processes = []
    for p in processes:
        new_p = dict(p)
        new_p['rt'] = p['bt']
        new_p['st'] = -1
        remaining_processes.append(new_p)
        
    current_time = 0
    completed = 0
    prev_id = None
    block_start = 0
    
    while completed < len(processes):
        available = [p for p in remaining_processes if p['at'] <= current_time and p['rt'] > 0]
        
        if len(available) == 0:
            if prev_id is not None:
                gantt.append({"id": prev_id, "start": block_start, "end": current_time})
                prev_id = None
                
            future_arrivals = [p['at'] for p in remaining_processes if p['rt'] > 0]
            next_arrival = min(future_arrivals)
            
            if prev_id != "Idle":
                block_start = current_time
                prev_id = "Idle"
                
            current_time = next_arrival
            continue
            
        # Sort by Priority, then Arrival Time, then ID
        available.sort(key=lambda x: (x['priority'], x['at'], int(x['id'][1:])))
        
        p = available[0]
        
        if prev_id != p['id']:
            if prev_id is not None:
                gantt.append({"id": prev_id, "start": block_start, "end": current_time})
            block_start = current_time
            prev_id = p['id']
            
        if p['st'] == -1:
            p['st'] = current_time
            
        future_arrivals = [r['at'] for r in remaining_processes if r['at'] > current_time and r['rt'] > 0]
        
        if len(future_arrivals) > 0:
            next_arrival = min(future_arrivals)
            time_to_run = min(p['rt'], next_arrival - current_time)
        else:
            time_to_run = p['rt']
            
        p['rt'] -= time_to_run
        current_time += time_to_run
        
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
        
    final_gantt = []
    for b in gantt:
        if len(final_gantt) > 0 and final_gantt[-1]['id'] == b['id']:
            final_gantt[-1]['end'] = b['end']
        else:
            final_gantt.append(b)
            
    return {"gantt": final_gantt, "metrics": metrics}


def round_robin(processes, time_quantum):
    gantt = []
    metrics = {}
    
    remaining_processes = []
    for p in processes:
        new_p = dict(p)
        new_p['rt'] = p['bt']
        new_p['st'] = -1
        remaining_processes.append(new_p)
        
    remaining_processes.sort(key=lambda x: (x['at'], int(x['id'][1:])))
    
    current_time = 0
    queue = []
    completed = 0
    i = 0 
    
    # Enqueue processes arriving at time 0
    while i < len(remaining_processes) and remaining_processes[i]['at'] <= current_time:
        queue.append(remaining_processes[i])
        i += 1
        
    prev_id = None
    block_start = 0
    
    while completed < len(processes):
        if len(queue) == 0:
            if prev_id is not None and prev_id != "Idle":
                gantt.append({"id": prev_id, "start": block_start, "end": current_time})
                
            next_arrival = remaining_processes[i]['at']
            if prev_id != "Idle":
                block_start = current_time
                prev_id = "Idle"
                
            current_time = next_arrival
            
            while i < len(remaining_processes) and remaining_processes[i]['at'] <= current_time:
                queue.append(remaining_processes[i])
                i += 1
            continue
            
        p = queue.pop(0)
        
        if prev_id != p['id']:
            if prev_id is not None:
                gantt.append({"id": prev_id, "start": block_start, "end": current_time})
            block_start = current_time
            prev_id = p['id']
            
        if p['st'] == -1:
            p['st'] = current_time
            
        time_to_run = min(p['rt'], time_quantum)
        p['rt'] -= time_to_run
        current_time += time_to_run
        
        # Check for arrivals during this execution block
        while i < len(remaining_processes) and remaining_processes[i]['at'] <= current_time:
            queue.append(remaining_processes[i])
            i += 1
            
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
        else:
            queue.append(p) 
            
    if prev_id is not None:
        gantt.append({"id": prev_id, "start": block_start, "end": current_time})
        
    final_gantt = []
    for b in gantt:
        if len(final_gantt) > 0 and final_gantt[-1]['id'] == b['id']:
            final_gantt[-1]['end'] = b['end']
        else:
            final_gantt.append(b)
            
    return {"gantt": final_gantt, "metrics": metrics}
