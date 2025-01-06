#write a program to remove specific words from a give list using lambda
lst = ["omer", "cohen", "test","no"]
to_remove = ["omer", "no"]
filer_list = list(filter(lambda word : word not in to_remove, lst))

print(filer_list)


#write a program to sort a list  of strings (numbers) numerically using lambda

numbers = ["53","32","1","90"]
sorted_numbers= sorted(numbers, key=lambda x: int(x))
print(type(sorted_numbers))


#write a program to calcuate the sum of positive and negative
#  numbers of a given list of numbers using lambda function
lst1 = [1,2,-3,30,-12]
negative_sum = sum(list(filter(lambda n: n < 0, lst1)))
positive_sum = sum(list(filter(lambda n: n > 0, lst1)))
print(positive_sum)
print(negative_sum)


#using list comprehension , construct a list from the sqquares of
#  each even elemn in the give list
numbers1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
square_of_even = [n**2 for n in numbers1 if n % 2 == 0]
print(square_of_even)


#write a function that receives the dictionary with name of products 
# and their prices and returns the dict with 10% sales

def products_after_sales(products):
    return {key : value * 0.9 for key,value in products.items()}
    

products = {
    "apple": 2.5,
    "banana": 1.2,
    "chocolate": 3.5,
    "bread": 1.8
}
print(products_after_sales(products))


#given a word in hebrew calculate the gimetria value

def gimetria_value(word):
    sum = 0
    gematria_dict = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9,
    'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60, 'ע': 70, 'פ': 80, 'צ': 90,
    'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400, 'ך' : 500, 'ם': 600
    , 'ן': 700,'ן': 700,'ף': 800,'ץ': 900}

    for letter in word:
        if letter in gematria_dict:
            sum += gematria_dict[letter]
    
    return sum

word = "שלום"
print(gimetria_value(word))



