import math

print("Shannon Compression Program")
print("=================================================================")
import collections

message = "alex papadas"              #taking input from user

def symProb(String):
    sc = dict(collections.Counter(String.upper()));
    return {k: v / sum(sc.values()) for k, v in sc.items()}

c = {}
def create_list(message):
    list = dict(collections.Counter(message))
    #for key, value in list.items():
        #print(key, ' : ', value)                         #creating the sorted list according to the probablity
    list_sorted = sorted(iter(list.items()), key = lambda k_v:(k_v[1],k_v[0]),reverse=True)
    final_list = []
    for key,value in list_sorted:
        final_list.append([key,value,''])
    return final_list


def divide_list(list):
    if len(list) == 2:
        #print([list[0]],[list[1]])               #printing merged pathways
        return [list[0]],[list[1]]
    else:
        n = 0
        for i in list:
            n+= i[1]
        x = 0
        distance = abs(2*x - n)
        j = 0
        for i in range(len(list)):               #shannon tree structure
            x += list[i][1]
            if distance < abs(2*x - n):
                j = i
    #print(list[0:j+1], list[j+1:])               #printing merged pathways
    return list[0:j+1], list[j+1:]


def label_list(list):
    list1,list2 = divide_list(list)
    for i in list1:
        i[2] += '0'
        c[i[0]] = i[2]
    for i in list2:
        i[2] += '1'
        c[i[0]] = i[2]
    if len(list1)==1 and len(list2)==1:        #assigning values to the tree
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

        letter_binary.append([key,value])

    for a in message:
        for key, value in code.items():
            if key in a:
                compressed_string = compressed_string + value

    H = 0
    for i in range(0, len(sv)): H = H + sv[i] * math.log((1 / sv[i]), 2);
    entropy = H

    return compressed_string,letter_binary,entropy





def decompress(string,letter_binary):
    bitstring = ""
    for digit in string:
        bitstring = bitstring + digit
    uncompressed_string =""
    code = ""
    for digit in bitstring:
        code = code+digit
        pos=0
        for letter in letter_binary:               # decoding the binary and genrating original data
            if code ==letter[1]:
                uncompressed_string = uncompressed_string+letter_binary[pos] [0]
                code=""
            pos+=1
    return uncompressed_string

compressed = compress("alex papadas")
print("compressed:")
print(compressed)
decompressed = decompress(compressed[0],compressed[1])
print("decompressed")
print(decompressed)