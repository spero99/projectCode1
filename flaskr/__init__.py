import collections
import os
import random
import json
from flask_socketio import SocketIO, send , emit
from flask import Flask, render_template,flash,request,redirect, url_for
from collections import Counter
import math
from collections import OrderedDict
from hashlib import sha256
import base64


def create_app(test_config=None):
    # create and configure the app
    UPLOAD_FOLDER = 'C:/test'
    ALLOWED_EXTENSIONS = {'txt'}

    app = Flask(__name__, instance_relative_config=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),

    )
    socket = SocketIO(app)


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route("/")
    def main():
        return render_template("main.html")

    @app.route('/', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            error = int( request.form.get("error"))
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], "data.txt"))
                with open('C:/test/data.txt', 'r') as file:
                    data = file.read().replace('\n', '')
                #compress.compressing(data)
                #socket.send(encoded_message)
                compressed_data = compress(data) #Compression of the data
                compressed_message = compressed_data[0]
                compressed_letter_binary = compressed_data[1]
                compressed_entropy = compressed_data[2]
                encoded_message = encode_message(compressed_message) #encoding of the data
                encoded_message_with_error = simulateError(encoded_message,error) #simulation of errors by noise during transmission
                based_message = encode_to_base64(encoded_message_with_error)#encode to base 64
                debased_message = decode_to_base64((based_message))
                write_Json(encoded_message_with_error,error,based_message, compressed_entropy) #creation of Json
                decoded_data = decode_message(debased_message) #decoding of the
                decoded_message = decoded_data[0]
                decoded_errors = decoded_data[1]
                decompressed_message = decompress(decoded_message,compressed_letter_binary)

                #hashed_decoded_message = hash(decoded_message)
                page_data = [{'original': data,
                              'compressed': compressed_message,
                              'compressed_entropy':compressed_entropy,
                              'encoded': encoded_message,
                              'based64': based_message,
                              'de_based64': debased_message,
                              'error': error,
                              'received': encoded_message_with_error,
                              'decoded_message': decoded_message,
                              'decoded_errors': decoded_errors,
                              'decompressed_message': decompressed_message
                              }]
        return render_template("results.html", data= page_data)



    @socket.on('receive_json')
    def handle_the_json(json):
        print('received json: ' + str(json))

    if __name__ == "__main__":
        socket.run(app)

    # ----------------------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------encode-------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------------------

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

        #print("\nGenerator Matrix (G):")
        for row in G:
            print(row)
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

    #-----------------------------------------------------------------------------------------------------------------------------
    #-------------------------------------------decode----------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------

    def decode_message(encoded_string):
        encoded_words =  [list(map(str, encoded_string[i:i + 7])) for i in range(0, len(encoded_string), 7)]

        generator_polynomial = [1, 1, 0, 1]  # G(x) = x^3 + x + 1
        k = 4  # Size of each original word in bits
        n = k + len(generator_polynomial) - 1  # Size of each encoded word
        counter = 0
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
        original_string = ''.join([''.join(word) for word in original_words])

        return original_string,counter

    #----------------------------------------------------------------------------------------------------------------------------------
    #-------------------------------------------compress-------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------------------

    def symProb(String):
        sc = dict(collections.Counter(String.upper()));
        return {k: v / sum(sc.values()) for k, v in sc.items()}

    c = {}
    def create_list(message):
        list = dict(collections.Counter(message))
        #for key, value in list.items():
            #print(key, ' : ', value)  # creating the sorted list according to the probablity
        list_sorted = sorted(iter(list.items()), key=lambda k_v: (k_v[1], k_v[0]), reverse=True)
        final_list = []
        for key, value in list_sorted:
            final_list.append([key, value, ''])
        return final_list

    def divide_list(list):
        if len(list) == 2:
            # print([list[0]],[list[1]])               #printing merged pathways
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
        # print(list[0:j+1], list[j+1:])               #printing merged pathways
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

    #-----------------------------------------error simulation/hash/json------------------------------------------------

    def simulateError(encoded_string,error):
        string_length = len(encoded_string)
        changed_bits = string_length * error // 100 # 5% error on sent simulation
        encoded_list = [i for i in encoded_string]
        affected_bits = () #not in use
        for i in range(changed_bits):
            bit = random.randint(0, string_length)
            if encoded_list[bit] == "0":
                encoded_list[bit] = "1"
            else:
                encoded_list[bit] = "0"

        encoded_string_with_error = "".join(str(element) for element in encoded_list)

        return encoded_string_with_error

    def hash(string):
        hashed_string = sha256(string.encode('utf-8').hexdigest())
        return hashed_string

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
    def write_Json(coded_message, errors, sha, entropy):

        dictionary = {
            'encoded_message': coded_message,
            'compression_algorithm: fano-shannon'
            'encoding: cyclic CRC-3'
            'parameters: generator_polynomial = x^3 + x + 1 '
            'errors': errors,
            'SHA256': sha,
            'entropy': entropy,
        }

        json_object = json.dumps(dictionary, indent=7)

        with open("coded.json", "w") as outfile:
            outfile.write(json_object)
    return app