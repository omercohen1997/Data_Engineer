""" import data_structures

#Create a Function to Check if a Name is Defined in the Global Namespace
def is_name_global(name):
    return name in globals()

name = "test"
print(is_name_global("name"))
print(is_name_global(name))


# Test data_structures module
# test_my_utils.py

def test_remove_non_str():
    my_list = [1, 'hello', 3.14, 'world', True, 'Python']
    data_structures.remove_non_str(my_list) == ['hello', 'world', 'Python']
    print("test_remove_non_str passed")

def test_count_letters():
    data_structures.count_letters("hello") == {'h': 1, 'e': 1, 'l': 2, 'o': 1}
    print("test_count_letters passed")

def test_count_letters_no_if():
    data_structures.count_letters_no_if("hello") == {'h': 1, 'e': 1, 'l': 2, 'o': 1}
    print("test_count_letters_no_if passed")

def test_unique_values():
    input_dict = {'a': 1, 'b': 2, 'c': 1, 'd': 3, 'e': 2}
    result = data_structures.unique_values(input_dict)
    sorted(result) == [1, 2, 3]  
    print("test_unique_values passed")

def test_left_rotation():
    lst = [1, 2, 3, 4, 5]
    result = data_structures.left_rotation(lst, 2)
    result == [3, 4, 5, 1, 2]
    print("test_left_rotation passed")

def test_remove_and_print_second():
    nums = [1, 2, 3, 4, 5]
    data_structures.remove_and_print_second(nums) 
    print("test_remove_and_print_second executed")

def test_dict_to_list_tuples():
    my_dict = {'a': 1, 'b': 2, 'c': 3}
    result = data_structures.dict_to_list_tuples(my_dict)
    result == [('a', 1), ('b', 2), ('c', 3)]
    print("test_dict_to_list_tuples passed")

def test_print_min_max():
    my_dict = {'a': 10, 'b': 20, 'c': 5, 'd': 15}
    data_structures.print_min_max(my_dict)  
    print("test_print_min_max executed")

if __name__ == "__main__":
    test_remove_non_str()
    test_count_letters()
    test_count_letters_no_if()
    test_unique_values()
    test_left_rotation()
    test_remove_and_print_second()
    test_dict_to_list_tuples()
    test_print_min_max()

 """


# create package

def find_missing_number(start, end,arr):
    sum = 0
    for i in range(start,end + 1):
        sum += i

    for n in arr:
        sum -= n
    return sum

arr = [4, 2, 5]
range_start = 2
range_end = 5
print(find_missing_number(range_start, range_end, arr))




