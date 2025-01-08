from priority_queue import PriorityQueue
import time
from typing import Coroutine

class Scheduler:
    def __init__(self):
        self.queue = PriorityQueue()

    def add(self, coroutine: Coroutine, delay):
        timepoint = time.time() + delay
        self.queue.push(coroutine, timepoint)

    def run(self):
        while not self.queue.is_empty():
            timepoint, coroutine = self.queue.pop()
            current_time = time.time()
            if current_time < timepoint:
                time.sleep(timepoint - current_time)

            try:
                interval = next(coroutine)
                  
                if isinstance(interval, (int, float)) and interval > 0:
                    next_timepoint = timepoint + interval
                    self.queue.push(coroutine, next_timepoint)
            except StopIteration:
                print("DONE")


            
            

if __name__ == "__main__":
    def variable_task():
        count = 0
        while count < 5:
            print(f"Task executing at count {count}")
            if count < 2:
                count += 1
                yield 2  # Run again in 2 seconds for first two executions
            else:
                count += 1
                yield 5  # Then wait 5 seconds between executions
    
    def countdown_task():
        for i in range(5, 0, -1):
            print(f"Countdown: {i}")
            yield i  # Wait i seconds before next execution
    
    scheduler = Scheduler()
    
    # Example usage
    scheduler.add(variable_task(), 1)  # Start after 1 second
    scheduler.add(countdown_task(), 0)  # Start immediately
    
    print("Running scheduler...")
    scheduler.run()