import random

def create_error(coded_message,n):
    s = list(coded_message)
    length = len(s)
    error_chance = ( n * length)/100
    for i in error_chance:
        bit = random.randint(0, length)
        if s[bit] == "0":
            s[bit] = "1"
        else:
            s[bit] = "0"