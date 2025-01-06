""" Question 1 
import math

class Point:
    def __init__(self,x=0.0, y=0.0):
        if not(isinstance(x,(int, float)) and isinstance(y,(int, float))):
            raise ValueError("x and y must be numbers.")
            
        self.x = x
        self.y = y
    
    def distance_from_origin(self):
         return math.sqrt(self.x ** 2 + self.y ** 2)    
        



try:
    p = Point(9.23, 2.5)
    print(p.x)
    print(p.y) 

    print(p.distance_from_origin())

    p1 = Point(9.23, '2.5')
    print(p1.x)
    print(p1.y) 

    print(p1.distance_from_origin())

    
except ValueError as e:
    print(f"Error: {e}") """
    
    
    
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        
    
class List:
    def __init__(self):
        self.head = None
        self.len = 0
    
    def push(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head  = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node
            
        self.len += 1
        
    def pop(self):
        if self.head is None:
            print("list is empty")
            return
        
        self.head = self.head.next
        self.len -= 1

        
    def head_value(self):
        if self.head is None:
            raise ValueError("List is empty")
        return self.head.data
    
    def __len__(self):
        return self.len
    
    def is_Empty(self):
        return self.head is None
    
    
    def __str__(self):
        if self.head is None:
            return "The list is empty."
        
        result = []
        current = self.head
        while current:
            result.append(str(current.data))
            current = current.next
        return " -> ".join(result) + " -> None"   


""" 
my_list = List()
my_list.push(10)
my_list.push(20)
my_list.push(30)

# Print the list using `__str__`
print(my_list)  # Output: 10 -> 20 -> 30 -> None

# After popping an element
my_list.pop()
print(my_list)  # Output: 20 -> 30 -> None
 """

class foo:
    def __init__(self,a,b):
        print("first init")
    def __init__(self,a,b,c):
        print("second init")
        
f = foo(1,2)
