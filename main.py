# Shortest Remaining Time (SRT) algorithm
# Create a Process class to represent a single process
class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid  # Process ID
        self.arrival_time = arrival_time  # Time of arrival
        self.burst_time = burst_time  # CPU time required by process
        self.priority = priority  # priority of the process
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.remaining_time = burst_time


# Implement the SRT function
def shortest_remaining_time(processes_data):
    # Convert the input data into Process objects
    # Sort them by arrival time
    processes = [Process(*p) for p in
                 processes_data]  # Creates a list of type Process for all processes in processes data
    processes.sort(key=lambda x: x.arrival_time)  # Sorting the processes by the key, a lambda (anonymous) variable, which is the arrival time

    # Initialize scheduling the variables
    current_time = 0  # Track current time in simulation
    completed_processes = []  # Store processes that have finished running
    ready_queue = []  # Store processes that have arrived but not completed
    gantt_chart = []  # Store the execution timeline

    # Check and add any newly arrived process to the ready queue
    def update_ready_queue():
        for process in processes:
            if (process.arrival_time <= current_time
                    and process not in ready_queue
                    and process not in completed_processes):
                ready_queue.append(process)

    # find out when the next process will arrive
    def get_next_arrival_time():
        # get all processes that are in the ready queue whose arrival time is in the future
        future_arrivals = [p.arrival_time for p in processes
                           if p.arrival_time > current_time and
                           p not in completed_processes]
        return min(future_arrivals) if future_arrivals else float('infinity')

    # Main scheduling algorithm - continue until all processes are completed
    while len(completed_processes) < len(processes):
        # Step 1: Update the ready queue with any newly arrived processes
        update_ready_queue()

        # Step 2: Handle the case when no processes are ready to execute
        if not ready_queue:
            # find the next process arrival time
            next_arrival = get_next_arrival_time()
            if current_time < next_arrival:
                # System idles
                gantt_chart.append(['IDLE', current_time, next_arrival])
                current_time = next_arrival
            continue

        # Step 3: Select the process with the shortest remaining time
        # If tied, we will use arrival time as the arbitration rule
        current_process = min(ready_queue, key=lambda p: (p.remaining_time, p.arrival_time))

        # Step 4: Calculate the time slice
        next_arrival = get_next_arrival_time()
        time_slice = min(current_process.remaining_time, next_arrival - current_time)

        # Step 5: Execute processes for the calculate time slice
        start_time = current_time  # records the start time
        current_time += time_slice  # advance the system clock
        current_process.remaining_time -= time_slice  # update remaining time

        # Step 6: check if process has completed
        if current_process.remaining_time == 0:
            # update completion metrics
            current_process.completion_time = current_time

            # turnaround time = completion time - arrival
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time

            # waiting time
            current_process.waiting_time = (current_process.turnaround_time - current_process.burst_time)

            # terminate the process
            # move it from the ready queue
            completed_processes.append(current_process)
            gantt_chart.append([str(current_process.pid), current_process.arrival_time, current_process.completion_time])
            ready_queue.remove(current_process)

    return completed_processes, gantt_chart


def print_results(completed_processes, gantt_chart):
    # Print formatted tables of metrics
    print("\nProcess Execution Order (Gantt Chart): ")
    print("-" * 50)
    for entry in gantt_chart:
        if entry[0] == "IDLE":
            # show period of idle
            print(f"IDLE: {entry[1]} -> {entry[2]}")
        else:
            # Show process execution periods
            print(f"P{entry[0]}: {entry[1]} -> {entry[2]}")

    # print the metric tables
    print("\nProcess Scheduling Details:")
    print("-" * 65)
    print("PID Arrival Burst Completion Turnaround Waiting")
    print("-" * 65)

    # Print metrics for each process sorted by their ID number
    for p in sorted(completed_processes, key=lambda x: x.pid):
        print(f"{p.pid:<5}{p.arrival_time:<9}{p.burst_time:<7}"
              f"{p.completion_time:<12}{p.turnaround_time:<12}"
              f"{p.waiting_time}")

    # calculate and print average metrics
    avg_turnaround = sum(p.turnaround_time for p in completed_processes) / len(completed_processes)
    avg_waiting = sum(p.waiting_time for p in completed_processes) / len(completed_processes)

    print("-" * 65)
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")
    print(f"Average Waiting Time: {avg_waiting:.2f}")


# process_id, arrival_time, burst_time, priority
process_list = [[1, 0, 3, 1, ],
                [2, 2, 6, 1],
                [3, 4, 4, 1],
                [4, 6, 5, 1],
                [5, 8, 2, 1]]

completed, gantt = shortest_remaining_time(process_list)
print_results(completed, gantt)
