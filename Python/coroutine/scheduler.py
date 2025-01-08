from priority_queue import PriorityQueue
import time
from typing import Callable

class Scheduler:
    def __init__(self):
        self.queue = PriorityQueue()

    def add(self, task: Callable, delay: float, frequency: float = None):
        timepoint = time.time() + delay  # Convert delay to absolute time
        self.queue.push((task, frequency), timepoint)

    def run(self):
        while not self.queue.is_empty():
            # Pop the next task and its scheduled time
            timepoint, (task, frequency) = self.queue.pop()
            
            current_time = time.time()
            # Wait until the task's scheduled time
            if current_time < timepoint:
                time.sleep(timepoint - current_time)

            # Execute the task
            is_repeat = task()

            # Reschedule if the task should repeat
            if is_repeat and frequency is not None and frequency > 0:
                next_timepoint = timepoint + frequency
                self.queue.push((task, frequency), next_timepoint)



if __name__ == "__main__":
    
    
    def task_1():
        print(f"Executing Task 1 at {time.strftime('%H:%M:%S')}")
        return True  # Repeat

    def task_2():
        print(f"Executing Task 2 at {time.strftime('%H:%M:%S')}")
        return False  # Do not repeat

    def task_3():
        print(f"Executing Task 3 at {time.strftime('%H:%M:%S')}")
        return True  # Repeat

    
    
    scheduler = Scheduler()

    # Add tasks
    scheduler.add(task_1, 2, frequency=5)  # Task 1 repeats every 5 seconds
    scheduler.add(task_2, 3)  # Task 2 runs once after 3 seconds
    scheduler.add(task_3, 4, frequency=10)  # Task 3 repeats every 10 seconds

    print("Running scheduler...")
    scheduler.run()
