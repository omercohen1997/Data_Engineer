import string

def create_alphabet_files():
    for letter in string.ascii_uppercase:
        name = letter + ".txt"
        with open(name, "w") as file:
            file.write(letter)
            
create_alphabet_files()