import collections
from collections import Counter
import math
from collections import OrderedDict
from hashlib import sha256
import base64
import random


def construct_generator_matrix(generator_polynomial, k):
    # Construct the generator matrix
    n = k + len(generator_polynomial) - 1
    G = []
    for i in range(k):
        row = [0] * i + generator_polynomial + [0] * (n - len(generator_polynomial) - i + 1)
        G.append(row[:n])
    return G


def divide_polynomials(dividend, divisor):
    # Perform polynomial division (mod 2) and return the remainder
    remainder = dividend[:]
    for i in range(len(dividend) - len(divisor) + 1):
        if remainder[i] == 1:  # Only perform operation if the bit is 1
            for j in range(len(divisor)):
                remainder[i + j] ^= divisor[j]
    return remainder[-(len(divisor) - 1):]


def format_polynomial(polynomial):
    terms = []
    for i, coeff in enumerate(polynomial):
        if coeff == 1:
            if i == 0:
                terms.append("1")
            elif i == 1:
                terms.append("x")
            else:
                terms.append(f"x^{i}")
    return " + ".join(terms)


def encode_message(message):
    # Fixed generator polynomial
    generator_polynomial = [1, 1, 0, 1]  # G(x) = x^3 + x + 1
    k = 4  # Size of each word in the message
    n = k + len(generator_polynomial) - 1  # Size of each encoded word

    # Convert the message into chunks of k bits
    chunks = [message[i:i + k] for i in range(0, len(message), k)]

    # Construct the generator matrix
    G = construct_generator_matrix(generator_polynomial, k)



    encoded_string = ""
    encoded_words = []
    for chunk in chunks:
        # Convert chunk to a polynomial (list of coefficients)
        M = [int(bit) for bit in chunk] + [0] * (len(generator_polynomial) - 1)
        # Calculate P(x) = M(x) * x^(n-k)
        P = M[:]
        # Calculate R(x) = P(x) mod G(x)
        R = divide_polynomials(P, generator_polynomial)
        # Form the encoded word
        encoded_word = M[:k] + R
        encoded_words.append(encoded_word)

        encoded_string = ""
    for word in encoded_words:
        encoded_string = encoded_string + ''.join(map(str, word))
    return encoded_string

def decode_message(encoded_string):
    #print("length is "+ str(len(encoded_string)))
    if len(encoded_string)%7 != 0 :
        #print("if")
        encoded_string = str(encoded_string) + "0"
        #print("new length is " + str(len(encoded_string)))
    encoded_words =[list(map(int, encoded_string[i:i + 7])) for i in range(0, len(encoded_string), 7)]
    #for word in encoded_words:
     #   print(len(word))

    generator_polynomial = [1, 1, 0, 1]  # G(x) = x^3 + x + 1
    k = 4  # Size of each original word in bits
    n = k + len(generator_polynomial) - 1  # Size of each encoded word
    counter = 0
    string= ""
    original_string = ""
    original_words = []
    for encoded_word in encoded_words:
        # Extract the first k bits of the encoded word
        original_word = encoded_word[:k]
        # Check for errors using the generator polynomial
        remainder = divide_polynomials(encoded_word, generator_polynomial)
        has_error = any(remainder)
        if has_error != 0:
            counter = counter + 1
        original_words.append(original_word)
    original_string = ''.join([''.join(str(word)) for word in original_words])
    for word in original_words:
        string = string + ''.join(map(str, word))
    original_string = str(string)


    return original_string,counter


def symProb(String):
    sc = dict(collections.Counter(String.upper()));
    return {k: v / sum(sc.values()) for k, v in sc.items()}

c = {}


def create_list(message):
    list = dict(collections.Counter(message))

    list_sorted = sorted(iter(list.items()), key=lambda k_v: (k_v[1], k_v[0]), reverse=True)
    final_list = []
    for key, value in list_sorted:
        final_list.append([key, value, ''])
    return final_list

def divide_list(list):
    if len(list) == 2:

        return [list[0]], [list[1]]
    else:
        n = 0
        for i in list:
            n += i[1]
        x = 0
        distance = abs(2 * x - n)
        j = 0
        for i in range(len(list)):  # shannon tree structure
            x += list[i][1]
            if distance < abs(2 * x - n):
                j = i

    return list[0:j + 1], list[j + 1:]

def label_list(list):
    list1, list2 = divide_list(list)
    for i in list1:
        i[2] += '0'
        c[i[0]] = i[2]
    for i in list2:
        i[2] += '1'
        c[i[0]] = i[2]
    if len(list1) == 1 and len(list2) == 1:  # assigning values to the tree
        return
    label_list(list2)
    return c

def compress(data):
    symd = symProb(data)  # symd-symbols Dictionary
    symdn = collections.OrderedDict(sorted(symd.items(), key=lambda kv: kv[1], reverse=True))
    sk = list(symdn.keys())
    sv = list(symdn.values())

    code = label_list(create_list(data))
    letter_binary = []
    compressed_string = ""
    for key, value in code.items():
        letter_binary.append([key, value])

    for a in data:
        for key, value in code.items():
            if key in a:
                compressed_string = compressed_string + value

    H = 0
    for i in range(0, len(sv)): H = H + sv[i] * math.log((1 / sv[i]), 2);
    entropy = H

    return compressed_string, letter_binary, entropy

def decompress(string, letter_binary):

    bitstring = ""
    for digit in string:
            bitstring = bitstring + digit
    uncompressed_string = ""
    code = ""
    for digit in bitstring:
        code = code + digit
        pos = 0
        for letter in letter_binary:  # decoding the binary and genrating original data
            if code == letter[1]:
                uncompressed_string = uncompressed_string + letter_binary[pos][0]
                code = ""
            pos += 1
    return uncompressed_string

def simulateError(encoded_string,error):
    encoded_string_with_error = ""
    if error == "0" :
        encoded_string_with_error == encoded_string
    else:
        string_length = len(encoded_string)
        changed_bits = string_length * error // 100 # % error on sent simulation


        changed_positions= random.sample(range(string_length), changed_bits)

        list_of_characters = [*encoded_string]

        for i in range(len(changed_positions)):
            if list_of_characters[changed_positions[i]] == "0":
                list_of_characters[changed_positions[i]] = "1"
            else:
                list_of_characters[changed_positions[i]] = "0"
        encoded_string_with_error = ''.join(list_of_characters)


    return encoded_string_with_error
def encode_to_base64(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

def decode_to_base64(string):
    base64_bytes = string.encode("ascii")

    sample_string_bytes = base64.b64decode(base64_bytes)
    decoded64_string = sample_string_bytes.decode("ascii")
    return decoded64_string


text = "this is a test for python project with fano shannon and crc-3"
error = 5
print(text)
compressed_data = compress(text)

compressed_message = compressed_data[0]
print("compressed message:" + compressed_message)

compressed_letter_binary = compressed_data[1]
compressed_entropy = compressed_data[2]
#print(compressed_letter_binary)
print ("test")
decompress_test = decompress(compressed_message, compressed_letter_binary)
print("decompressed test:" + decompress_test)

encoded_message = encode_message(compressed_message) #encoding of the data
print("encoded message:" + encoded_message)

encoded_message_with_error = simulateError(encoded_message,error) #simulation of errors by noise during transmission
print("encoded message with error:" + encoded_message_with_error)


based_message = encode_to_base64(encoded_message_with_error)#encode to base 64
print("based:" + based_message)
debased_message = decode_to_base64((based_message))
print("debased:" + debased_message)


decoded_data = decode_message(debased_message) #decoding of the
#decoded_data = decode_message(encoded_message) #decoding of the

decoded_message = decoded_data[0]
decoded_errors = decoded_data[1]
print("decode message:" + decoded_message)


print("decode errors:" + str(decoded_errors))

decompressed_message = decompress(decoded_message,compressed_letter_binary)
print("decompressed:" + decompressed_message)










print(compressed_message)
print(decoded_message)
if encoded_message_with_error == debased_message:
    print("yay")
if  compressed_message == decompressed_message:
    print("double yay")