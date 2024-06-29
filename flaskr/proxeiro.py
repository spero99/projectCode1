import random

import compress
encoded_string= "100100111110101000101001000101010101001010101010110101010101010001111100000111101101010010110011"
print(encoded_string)
string_length = len(encoded_string)
print("length")
print(string_length)
changed_bits = string_length * 5 // 100
print("errors")
print(changed_bits)
encoded_list= [i for i in encoded_string]
affected_bits = ()
for i in range(changed_bits):
    bit = random.randint(0, string_length)
    print(bit)
    print("^ bit with error")
    if encoded_list[bit] == "0":
        encoded_list[bit] = "1"
    else:
        encoded_list[bit] = "0"

encoded_string = "".join(str(element) for element in encoded_list)
print(encoded_string)


#string1 = input("write a string")
#compress.compressing(string1)
