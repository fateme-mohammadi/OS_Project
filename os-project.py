import matplotlib.pyplot as plt
import numpy as np
from collections import deque


class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_ratio = 0.0

def FCFS():
    # Code for First Come First Served (FCFS) scheduling algorithm
    n = len(processes)
    gantt_chart = []
    current_time = 0
    completed_processes = []
    at = []
    sorted_p = sorted(processes, key=lambda x: (x.arrival_time))
    
    while len(completed_processes) < n:
        eligible_processes = [p for p in sorted_p if p.arrival_time <= current_time]

        if eligible_processes:
             for i in range (len(eligible_processes)):
                current_process = eligible_processes[i]    
                current_process.waiting_time = current_time - current_process.arrival_time
                current_process.turnaround_time = current_process.waiting_time + current_process.burst_time

                at.append(current_process.arrival_time)
                completed_processes.append(current_process)
                gantt_chart.append((current_process.pid, current_time, current_process.burst_time))
                sorted_p.remove(current_process)
                current_time += current_process.burst_time

        else:
            current_time += 1  # No eligible processes, move to the next time unit
            

    total_waiting_time = sum(p.waiting_time for p in completed_processes)
    total_turnaround_time = sum(p.turnaround_time for p in completed_processes)
    avg_waiting_time = total_waiting_time / n
    avg_turnaround_time = total_turnaround_time / n
    
    print("\n")
    print("Process\t  Arrial Time\t  Burst Time\t  Waiting Time\t  Turn Around Time")
    for process in processes:
        print(f"{process.pid}\t{process.arrival_time}\t\t{process.burst_time}\t\t{process.waiting_time}\t\t{process.turnaround_time}")
        
    print(f"\nAverage Waiting Time: {avg_waiting_time}")
    print(f"\nAverage Turn Around Time: {avg_turnaround_time}")
    plot_gantt_chart(gantt_chart ,at)

    return avg_waiting_time

def SPN():
    # Code for SPN scheduling algorithm
    n = len(processes)
    sorted_processes = sorted(processes, key=lambda x: (x.arrival_time, x.burst_time))

    current_time = 0
    completed_processes = []
    gantt_chart = []
    at = []
    
    while len(completed_processes) < n:
        eligible_processes = [p for p in sorted_processes if p.arrival_time <= current_time and p not in completed_processes]

        if not eligible_processes:
            current_time = sorted_processes[0].arrival_time
            continue

        selected_process = min(eligible_processes, key=lambda x: x.burst_time)
        selected_process.waiting_time = current_time - selected_process.arrival_time
        selected_process.turnaround_time = selected_process.waiting_time + selected_process.burst_time
        
        completed_processes.append(selected_process)
        sorted_processes.remove(selected_process)
        
        total_waiting_time = sum(p.waiting_time for p in completed_processes)
        total_turnaround_time = sum(p.turnaround_time for p in completed_processes)
        avg_waiting_time = total_waiting_time / n
        avg_turnaround_time = total_turnaround_time / n

        at.append(selected_process.arrival_time)
        gantt_chart.append((selected_process.pid, current_time, selected_process.burst_time))
        current_time += selected_process.burst_time

    print("P\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time")
    for process in processes:
        print(f"{process.pid}\t{process.arrival_time}\t\t{process.burst_time}\t\t{process.waiting_time}\t\t{process.turnaround_time}")
    
    print(f"\nAverage Waiting Time: {avg_waiting_time}")
    print(f"\nAverage Turn Around Time: {avg_turnaround_time}")
    plot_gantt_chart(gantt_chart, at)

    return avg_waiting_time


def calculate_response_ratio(process, current_time):
    wait_time = current_time - process.arrival_time
    response_ratio = (wait_time + process.burst_time) / process.burst_time
    return response_ratio

def HRRN():
    # Code for HRRN scheduling algorithm
    n = len(processes)
    current_time = 0
    completed_processes = []
    gantt_chart = []
    at = []
    
    while len(completed_processes) < n:
        eligible_processes = [p for p in processes if p.arrival_time <= current_time and p not in completed_processes]
        
        if eligible_processes:
            response_ratios = [calculate_response_ratio(p, current_time) for p in eligible_processes]
            max_ratio_index = response_ratios.index(max(response_ratios))
            current_process = eligible_processes[max_ratio_index]
            
            current_process.waiting_time = current_time - current_process.arrival_time
            current_process.turnaround_time = current_process.waiting_time + current_process.burst_time
            current_process.response_ratio = calculate_response_ratio(current_process, current_time)
            
            gantt_chart.append((current_process.pid, current_time, current_process.burst_time))
            at.append(current_process.arrival_time)
            current_time += current_process.burst_time
            completed_processes.append(current_process)
        else:
            current_time += 1  # No eligible processes, move to the next time unit
    
    total_waiting_time = sum(p.waiting_time for p in completed_processes)
    total_turnaround_time = sum(p.turnaround_time for p in completed_processes)
    avg_waiting_time = total_waiting_time / n
    avg_turnaround_time = total_turnaround_time / n
   
    print("P\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time")
    for process in completed_processes:
        print(f"{process.pid}\t{process.arrival_time}\t\t{process.burst_time}\t\t{process.waiting_time}\t\t{process.turnaround_time}")
    
    print(f"\nAverage Waiting Time: {avg_waiting_time}")
    print(f"\nAverage Turn Around Time: {avg_turnaround_time}")
    plot_gantt_chart(gantt_chart, at)

    return avg_waiting_time


def round_robin(q):
    # Code for Round Robin scheduling algorithm
    n = len(processes)
    queue = deque(processes)
    current_time = 0
    completed_processes = []
    gantt_chart = []
    at = []

    while queue:
        current_process = queue.popleft()

        if current_process.remaining_time <= q:
            # Process completes within time quantum
            start_time = max(current_time, current_process.arrival_time)
            end_time = start_time + current_process.remaining_time
            current_process.remaining_time = 0
        else:
            # Process needs more than time quantum
            start_time = max(current_time, current_process.arrival_time)
            end_time = start_time + q
            current_process.remaining_time -= q
            # Put the process back in the queue for the next round
            queue.append(current_process)

        current_process.turnaround_time = end_time - current_process.arrival_time
        current_process.waiting_time = start_time - current_process.arrival_time
        current_time = end_time
                
        completed_processes.append(current_process)
        at.append(current_process.arrival_time)
        gantt_chart.append((current_process.pid, start_time, end_time - start_time))

    total_waiting_time = sum(p.waiting_time for p in completed_processes)
    total_turnaround_time = sum(p.turnaround_time for p in completed_processes)
    avg_waiting_time = total_waiting_time / n
    avg_turnaround_time = total_turnaround_time / n
    

    print("P\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time")
    for process in processes:
        print(f"{process.pid}\t{process.arrival_time}\t\t{process.burst_time}\t\t{process.waiting_time}\t\t{process.turnaround_time}")
    
    print(f"\nAverage Waiting Time: {avg_waiting_time}")
    print(f"\nAverage Turn Around Time: {avg_turnaround_time}")
    plot_gantt_chart(gantt_chart, at)

    return avg_waiting_time

    
    
def SRTF(q):
    # Code for SRTF scheduling algorithm
    n = len(processes)
    current_time = 0
    completed_processes = 0
    process_queue = []
    gantt_chart = []
    at = []
    
    while completed_processes < n:
        eligible_processes = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]

        if not eligible_processes:
            current_time += 1
            continue

        shortest_process = min(eligible_processes, key=lambda x: x.remaining_time)

        # Check quantum time
        quantum_run_time = min(q, shortest_process.remaining_time)
        shortest_process.remaining_time -= quantum_run_time

        if not process_queue or process_queue[-1] != shortest_process:
            process_queue.append(shortest_process)

        current_time += quantum_run_time

        if shortest_process.remaining_time == 0:
            completed_processes += 1
            process_queue.pop()
            shortest_process.waiting_time = current_time - shortest_process.arrival_time            
            shortest_process.turnaround_time = shortest_process.waiting_time + shortest_process.burst_time

        gantt_chart.append((shortest_process.pid, current_time - quantum_run_time, quantum_run_time))
        at.append(shortest_process.arrival_time)
                    
    total_turnaround_time = sum(process.turnaround_time for process in processes)
    total_waiting_time = sum(process.waiting_time for process in processes)

    avg_turnaround_time = total_turnaround_time / n
    avg_waiting_time = total_waiting_time / n


    print("P\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time")
    for process in processes:
        print(f"{process.pid}\t{process.arrival_time}\t\t{process.burst_time}\t\t{process.waiting_time}\t\t{process.turnaround_time}")
    
    print(f"\nAverage Waiting Time: {avg_waiting_time}")
    print(f"\nAverage Turn Around Time: {avg_turnaround_time}")
    plot_gantt_chart(gantt_chart, at)

    return avg_waiting_time


def plot_gantt_chart(gantt_chart, at):
    n = len(processes)
    fig, gnt = plt.subplots()
    
    for i, (pid, current_time, burst_time) in enumerate(gantt_chart):
        gnt.broken_barh([(current_time, burst_time)], (1*i, 0.5), facecolors='tab:blue')
        gnt.text(current_time + (burst_time/2), i + 0.25, f'P{pid}', ha='center', va='center')

    for i, (arrival_time) in enumerate(at):
        plt.scatter(arrival_time, i, label= "stars", color= "k", marker= "*", s=50)

    plt.grid(True)
    plt.yticks(range(len(gantt_chart)), [f'P{process_id}' for process_id, _, _ in gantt_chart])
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Processes')
    gnt.set_title('Gantt Chart')
    plt.savefig("gantt.png")
    plt.show()

def compare_scheduling_algorithms():
    avg = []  

    avg.append(FCFS())
    avg.append(SPN())
    avg.append(HRRN())
    avg.append(round_robin(10))
    #avg.append(SRTF(10))

    min_waiting_time = min(avg)
    ind = avg.index(min_waiting_time)
    print('\n')
    print("\nComparison of Average Waiting Times:")
    for i, avg_time in enumerate(avg):
        print(f"Average Waiting Time for Algorithm {i+1}: {avg_time}")
    print("\n")
    print(f"Minimum Waiting Time {min_waiting_time} that for Algoritm {ind+1}")
    


def get_user_input():
    processes = []
    cbt=[]
    at=[]
    print("Enter the number of process: ")
    n = int(input())
    print("Enter the arrival time of the processes: \n")
    at = [int(i) for i in input().split()]
    print("Enter the combinational burst time of the processes: \n")
    cbt = [int(i) for i in input().split()]

    for i in range(n):
        pid = i+1
        arrival_time = at[i]
        burst_time = cbt[i]

        process = Process(pid, arrival_time, burst_time)
        processes.append(process)

    return processes


# Ask the user to choose a scheduling algorithm
print("Choose a scheduling algorithm:")
print("1. FCFS")
print("2. SPN")
print("3. HRRN")
print("4. Round Robin")
print("5. SRTF")
print("6. compare wating time")
choice = int(input("Enter your choice (1-6): "))


# Example usage
if __name__ == '__main__':
    #processes = get_user_input()
    processes = [
        Process(1, 1, 10),
        Process(2, 2, 29),
        Process(3, 3, 3),
        Process(4, 4, 7),
        Process(5, 5, 12)
        ]
'''
        Process(1, 1, 10),
        Process(2, 2, 29),
        Process(3, 3, 3),
        Process(4, 4, 7),
        Process(5, 5, 12)

        
        Process(1, 1, 3),
        Process(2, 3, 6),
        Process(3, 5, 8),
        Process(4, 7, 4),
        Process(5, 8, 5),
'''

# Execute the selected scheduling algorithm
if choice == 1:
    FCFS()
elif choice == 2:
    SPN()
elif choice == 3:
    HRRN()
elif choice == 4:
    print('Please enter time quantum:')
    q = int(input())
    round_robin(q)
elif choice == 5:
    print('Please enter time quantum:')
    q = int(input())
    SRTF(q)
elif choice == 6:
    compare_scheduling_algorithms()
else:
    print("Invalid choice!")

