# name: login_password
# author: Smirnov Kirill
# revision: 2.2
# revision date: 17.10.2016
# description: this script is prototype for authorization and registration system, which hold its users and "passwords" in two separated files. actually it don't hold any passwords: only salted-md5hashes of them.
# todo: file_to_dict() - awful method, should rewrite


import hashlib
import ast
from random import randint


# constants
login_salt = "help_txt/login_salt.txt"
salt_hash = "help_txt/salt_hash.txt"


# detects, what should it do
def actionf():
    action = input(">")
    if action == '1':
        registration()
    elif action == '2':
        authorization()
    elif action == '0':
        print("good bye!")
        exit(0)
    else:
        return False


# changes file to dict
def file_to_dict(filename):
    value_dict = False
    with open(filename, 'r') as data_obj:
        data_str = data_obj.read()
        data_list = data_str.split('{')
        data_list.pop(0)
        data_str = str(data_list)
        data_str = data_str.replace('[', '')
        data_str = data_str.replace(']', '')
        data_str = data_str[1:-1]
        data_str = "{" + data_str
        data_dict = ast.literal_eval(data_str)
    data_obj.close()
    return data_dict


# finds value in file by given keyword
def find_in_file(filename, wat_look):
    data_dict = file_to_dict(filename)
    if wat_look in data_dict:
        value_file = data_dict[wat_look]
        return value_file
    else:
        return False


# writes new key&value to dict
def new_to_dict(data_dict, wat_right_key, wat_right_value):
    data_dict[wat_right_key] = wat_right_value
    return data_dict


# writes to file new key&value
def new_to_file(filename, wat_right_key, wat_right_value):
    data_dict = file_to_dict(filename)
    new_to_dict(data_dict, wat_right_key, wat_right_value)
    with open(filename, 'w') as data_obj:
        data_str = str(data_dict)
        data_obj.write(data_str)
    data_obj.close()


# salts
def megasalt():
    salt1 = randint(0, 1000)
    salt1 = str(salt1)
    salt1 = str.encode(salt1)
    salt1 = hashlib.md5(salt1).hexdigest()
    salt1 = str(salt1)
    return salt1


# hashes
def megahash(pass1, salt1):
    pass_salt1 = pass1 + salt1
    pass_salt1 = str.encode(pass_salt1)
    hash1 = hashlib.md5(pass_salt1).hexdigest()
    return hash1


# registrate new user
def registration():
    # input name & password
    print ("gimme yor name:")
    login1 = input(">")
    print ("gimme yor pass:")
    pass1 = input(">")
    # salt, hash
    salt1 = megasalt()
    hash1 = megahash(pass1, salt1)
    # write login-salt to file
    new_to_file(login_salt, login1, salt1)
    # write salt-hash to file
    new_to_file(salt_hash, salt1, hash1)
    # bye-bye message
    print ("thanks for registration!\n")


# authorize present user
def authorization():
    # input name
    print ("gimme yor name:")
    login2 = input(">")
    # find real salt
    salt2 = find_in_file(login_salt, login2)
    if salt2:
        print ("gimme yor pass:")
        pass2 = input(">")
        # find real hash
        hash2 = find_in_file(salt_hash, salt2)
        # find checking hash
        hash3 = megahash(pass2, salt2)
        # sravni hashi 2&3
        if hash2 == hash3:
            print ("thanks for authorization!\n")
            return True
        else:
            print ("you are fraud!\n")
            return False
    else:
        print ("you are fraud!\n")


# main
while True:
    print("whatcha gonna do?\n registration(1)\n authorization(2)\n exit(0)")
    action = actionf()
