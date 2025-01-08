from priority_queue import PriorityQueue

class Scheduler:
    
    def __init__(self):
        self._pq = PriorityQueue()

    
    def add(self, callback, time):
        self._pq.push(callback, time)
    
    
def run(self):
    while not self.queue.is_empty():
        priority, task = self.queue.pop()
        current_time = time.time()
        if current_time < priority:
            time.sleep(priority - current_time)
        task()

            
            
            

if __name__ == "__main__":
    scheduler = Scheduler()
    
    scheduler.add(lambda: print("i should be first"), 1)
    scheduler.add(lambda: print("i should be third"), 3)
    scheduler.add(lambda: print("i should be second"), 2)
    
    scheduler.run()