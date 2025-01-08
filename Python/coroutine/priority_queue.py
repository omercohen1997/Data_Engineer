class PriorityQueue:
    def __init__(self):
        self.__queue = []
        
        
    def push(self, item, priority):
        self.__queue.append((priority, item))
        self.__queue.sort(key=lambda x: x[0])
        
    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from an empty priority queue")
        return self.__queue.pop(0)[1]
    
    
    def peek(self):
         if self.is_empty():
            raise IndexError("Peek from an empty priority queue")
         return self.__queue[0][1]
        
    def is_empty(self):
        return len(self.__queue) == 0

    def __len__(self):
        return len(self.__queue)
    
    def __iter__(self):
        for priority, item in self.__queue:
            yield (priority, item)
    
    
if __name__ == "__main__":
    pq = PriorityQueue()
        
    def task_1():
        print("Executing Task 1")

    def task_2():
        print("Executing Task 2")

    def task_3():
        print("Executing Task 3")
    
    pq.push(task_1, 3)
    pq.push(task_2, 1)
    pq.push(task_3, 2)
    
    while not pq.is_empty():
        task = pq.pop()
        print(task)
        