#name: big_digits
#author: Smirnov Kirill
#revision: 1.1
#revision date: 11.11.2015
#description: this script prints digits, that user has input, in format of pseudo-digits, and they're BIG.


from digits_itself import *
symbols_to_replace = '[]\','


#reads input from keyboard, clear from non digits, returns number as a string
def getnums ():
    print ("print the number you wanna print")
    dirty_number = input (">")
    clear_number = ''
    for letter in dirty_number:
        try:
            letter = int(letter)
            clear_number = clear_number + str(letter)
        except Exception:
            clear_number = clear_number
    return clear_number

def replace_symbols (big_digit, replacement):
    replaced_symbols = []
    for line in big_digit:
        replaced_line = line.replace('*', replacement)
        replaced_symbols.append(replaced_line)
    return replaced_symbols

#transforms number to list of big symbols
def getlist (clear_number):
    list_of_digits = []
    for i in clear_number:
        replaced_symbols = replace_symbols (big_digits[int(i)], i)
        list_of_digits.append(replaced_symbols)
    return list_of_digits

def printing (list_of_digits):
    """function prints list of ints
    in format of big digits"""
    for i in range (0, letter_height):
        one_line = []
        for one_digit in list_of_digits:
            one_line.append(one_digit[i])
        one_line = str(one_line)
        for sym in symbols_to_replace:
            one_line = one_line.replace(sym, '')
        print (one_line)


clear_number = getnums()
list_of_digits = getlist(clear_number)
printing (list_of_digits)