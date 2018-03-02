# name: random_matrix
# author: Smirnov Kirill
# revision: 1.1
# revision date: 17.10.2016
# description: this script makes and prints matrix of random numbers...
# todo: calc some characteristics of matrix you've got
# todo: beatify output (string format fullfil, etc)


import random


def clean_num():
    dirty_num = input(">")
    try:
        clean_num = int(dirty_num)
        if (1 > clean_num or clean_num > 50):
            clean_num = 1
            print ("thats too small or big, try again")
    except Exception:
        clean_num = 1
        print ("thats not number, try again")
    return clean_num


def get_num():
    clean_row = 1
    clean_col = 1
    print ("print the number of rows")
    while clean_row == 1:
        clean_row = clean_num()
    print ("print the number of columns")
    while clean_col == 1:
        clean_col = clean_num()
    matrix_size = [clean_row, clean_col]
    return matrix_size


def random_matrix():
    print ("we gonna print matrix of random numbers")
    matrix_size = get_num()
    print ("we gonna print such big matrix: %d x %d" %
           (matrix_size[0], matrix_size[1]))
    matrix = []
    for i in range(0, matrix_size[0]):
        matrix_string = []
        for j in range(0, matrix_size[1]):
            x = random.randint(-100, 100)
            matrix_string.append(x)
        matrix.append(matrix_string)
        print (matrix_string)


random_matrix()
