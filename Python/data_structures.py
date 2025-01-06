'''

a = 1
b = 1
print(a == b, a is b)


a = 55555
b = 55555
print(a == b, a is b)


a = ()
b = ()
print(a == b, a is b) # because empty tuples are interned (tuples are immutable so it makes sense) so both pointing to the same memory


a = (1,2,3)
b = (1,2,3)
print(a == b, a is b)


a = [] 
b = []
print(a == b, a is b) # because lists are mutable so a and b don't have the same memory address

a = [1,2,3] 
b = a[:]  # list is mutable therefore it creates a new list object 
print(a == b, a is b)


x = [1,2,3]
y = x # y and x have the same address
y[0] = 8
print(x) 

x = (1,2,3)
y = x 
#y[0] = 8 # won't work because tuple is immutable
print(x) 


x = 1
y = x
y = 2 
print(x)

a = None # None is a singleton object which means there is only one instance of 
# None in memory
b = None
print(id(a) == id(b))

x = 'devops'
print(x[-1:-2]) # empty
print(x[3:-2])
print(x[::1])
print(x[::3])
print(x[1:2:3])
print(x[::-1])
print(x[1::-1])

'''

 
# Exercise
# create a function that receives list and removes all the non str objects from it

def remove_non_str (list):
    return [item for item in list if isinstance(item, str)]

my_list = [1, 'hello', 3.14, 'world', True, 'Python']
cleaned_list = remove_non_str(my_list)
print(cleaned_list)  


def count_letters(str):
    dict = {}
    for c in str:
        if c not in dict:
            dict[c] = 1
        else:
            dict[c] += 1
    return dict
'''
str = "hello"
result = count_letters(str)
print(result)  # Output: {'h': 1, 'e': 1, 'l': 2, 'o': 1}
'''



def count_letters_no_if(str):
    dict = {}
    for c in str:
       dict[c] = dict.get(c, 0) + 1
    return dict
'''

str = "hello"
result = count_letters_no_if(str)
print(result)  # Output: {'h': 1, 'e': 1, 'l': 2, 'o': 1}
'''




def unique_values(dict):
    return list(set(dict.values()))
'''

input_dict = {'a': 1, 'b': 2, 'c': 1, 'd': 3, 'e': 2}
result = unique_values(input_dict)
print(result)  # Output: [1, 2, 3]
'''



def left_rotation(lst, n):
     return lst[n:] + lst[:n]
'''

lst = [1, 2, 3, 4, 5]
n = 2
result = left_rotation(lst, n)
print(result)  # Output: [3, 4, 5, 1, 2]
'''



def remove_and_print_second(lst):
    while len(lst) > 1:
        print(lst[1])
        lst.pop(1)  
        
        if lst:  
            lst.append(lst.pop(0))  
'''

nums = [1, 2, 3, 4, 5]
remove_and_print_second(nums)
'''



def dict_to_list_tuples(dict):
    lst = []
    
    for key, value in dict.items():
        lst.append((key,value))
    return lst

'''

my_dict = {'a': 1, 'b': 2, 'c': 3}
result = dict_to_list_tuples(my_dict)
print(result)
'''


def print_min_max(dict):
    max_key = None
    min_key = None
    max_val =  float('-inf')    
    min_val = float('inf')

    for key, value in dict.items():
        if value > max_val:
            max_val = value
            max_key = key
        if value < min_val:
            min_val = value
            min_key = key 

    print(f"The max value of key {max_key} is {max_val}")
    print(f"The max value of key {min_key} is {min_val}")

'''

my_dict = {'a': 10, 'b': 20, 'c': 5, 'd': 15}
print_min_max(my_dict)

'''

