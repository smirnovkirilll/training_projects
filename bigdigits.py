#name: big_digits
#author: Smirnov Kirill
#revision: 1.0
#revision date: 06.11.2015
#description: this script prints digits, that user has input, in format of pseudo-digits, and they're BIG.


from digits_itself import *


def getnums ():
    """function read from keyboard,
    clear from non digits"""
    print ("print the nymber you wanna print")
    dirty_number = input (">")
    clear_number = ""
    for letter in dirty_number:
        try:
            letter = int(letter)
            clear_number = clear_number + str(letter)
        except Exception:
            clear_number = clear_number
    return clear_number


def getlist (clear_number):
    list_of_digits = []
    for letter in clear_number:
        if int(letter) == 0:
            list_of_digits.append(big_digits[0])
        elif int(letter) == 1:
            list_of_digits.append(big_digits[1])
        elif int(letter) == 2:
            list_of_digits.append(big_digits[2])
        elif int(letter) == 3:
            list_of_digits.append(big_digits[3])
        elif int(letter) == 4:
            list_of_digits.append(big_digits[4])
        elif int(letter) == 5:
            list_of_digits.append(big_digits[5])
        elif int(letter) == 6:
            list_of_digits.append(big_digits[6])
        elif int(letter) == 7:
            list_of_digits.append(big_digits[7])
        elif int(letter) == 8:
            list_of_digits.append(big_digits[8])
        elif int(letter) == 9:
            list_of_digits.append(big_digits[9])
    return list_of_digits


def printing (list_of_digits):
    """function prints list of ints
    in format of big digits"""
    for i in range (0, letter_height):
        one_line = []
        for one_digit in list_of_digits:
            one_line.append(one_digit[i])
        one_line = str(one_line)
        one_line = one_line.replace("\'", "")
        one_line = one_line.replace(",", "")
        one_line = one_line.replace("[", "")
        one_line = one_line.replace("]", "")
        print (one_line)


clear_number = getnums()
list_of_digits = getlist(clear_number)
printing(list_of_digits)