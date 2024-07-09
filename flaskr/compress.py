from collections import Counter
import math
from collections import OrderedDict




def symProb(String):
    sc = dict(Counter(String.upper()));
    return {k: v / sum(sc.values()) for k, v in sc.items()}

def compressing(string):
    def best_partition(initial, final):
        pts = []  # points
        for i in range(initial + 1, final):
            diff = abs(sum(sv[initial:i]) - sum(sv[i:final]))
            pts.append((diff))
            # print(abs(sum(sv[initial:i])-sum(sv[i:final])),sv[initial:i],sv[i:final],i)
            # print("\n",[sum(sv[initial:i]),sum(sv[i:final])],"\n")
        #print(pts.index(min(pts)) + initial)

        if pts.index(min(pts)) < initial:
            return pts.index(min(pts)) + initial;
        else:
            return pts.index(min(pts))

    def up(initial, final):
        for i in range(initial, final): sc[i] = sc[i] + '0'

    def down(initial, final):
        for i in range(initial, final): sc[i] = sc[i] + '1'

    symd = symProb(string)  # symd-symbols Dictionary
    symdn = OrderedDict(sorted(symd.items(), key=lambda kv: kv[1], reverse=True))
    sk = list(symdn.keys())
    sv = list(symdn.values())

    initial = 0
    final = len(sv)
    sc = [''] * (len(sv))
    current_index = [(initial, final)]
    new_index = []
    stage = 1
    while current_index != []:
        #print("---", "stage:-", stage, "----");
        #print(sc);
        new_index = [];
        #print(current_index)
        for index in current_index:
            if (index[1] - index[0]) == 2: sc[index[0]] = sc[index[0]] + '0'; sc[index[1] - 1] = sc[index[1] - 1] + '1';

            if (index[1] - index[0]) > 2:
                index_ptr = best_partition(index[0], index[1]) + 1;
                new_index.append((index[0], index_ptr));
                up(index[0], index_ptr);
                new_index.append((index_ptr, index[1]));
                down(index_ptr, index[1]);
            current_index = new_index
        stage = stage + 1
    # for last stage
    if current_index == []:
        #print("---", "stage:-", stage, "----");
        #print(sc);
        new_index = [];
        #print(current_index)

    # In[9]:

    dummy = []
    for i in range(0, len(sv)): dummy.append((sk[i], sc[i]));
    encoded_dictionary = OrderedDict(dummy)

    # In[10]:

    data = {'Symbol': sk, 'probability': sv, 'codeword': sc, }
    df = pd.DataFrame(data)
    df.head(len(sk))

    # # Encoded Message
    # In[11]:
    compressed_message = ''.join(sc)
    print("For message:-", string, "\nEncoded message is:-", compressed_message)

    # # Entropy Calculation:-
    # In[12]:

    H = 0
    for i in range(0, len(sv)): H = H + sv[i] * math.log((1 / sv[i]), 2);
    entropy = H
    print("Entropy is:-", H, "bits/message")

    # # Average Codeword Length
    # In[13]:

    L = 0
    for i in range(0, len(sc)): L = L + len(sc[i]) * sv[i];
    avg_length = L
    print("Average Codeword length is:-", L, "bits/message")

    # # Compression

    # In[14]:

    code_efficiency = (H / L) * 100
    print("Coding efficiency is :-", (H / L) * 100)

    def best_partition(initial, final):
        pts = []  # points
        for i in range(initial + 1, final):
            diff = abs(sum(sv[initial:i]) - sum(sv[i:final]))
            pts.append((diff))
            # print(abs(sum(sv[initial:i])-sum(sv[i:final])),sv[initial:i],sv[i:final],i)
            # print("\n",[sum(sv[initial:i]),sum(sv[i:final])],"\n")
        #print(pts.index(min(pts)) + initial)

        if pts.index(min(pts)) < initial:
            return pts.index(min(pts)) + initial;
        else:
            return pts.index(min(pts))

    def up(initial, final):
        for i in range(initial, final): sc[i] = sc[i] + '0'

    def down(initial, final):
        for i in range(initial, final): sc[i] = sc[i] + '1'


    return compressed_message,entropy,avg_length



