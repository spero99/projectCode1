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
                compressed_data = compressing(data) #Compression of the data
                compressed_message = compressed_data[0]
                compressed_entropy = compressed_data[1]
                encoded_message = encode_message(compressed_message) #encoding of the data
                encoded_message_with_error = simulateError(encoded_message,error) #simulation of errors by noise during transmission
                based_message = encode_to_base64(encoded_message_with_error)#encode to base 64
                debased_message = decode_to_base64((based_message))
                #hashed_message = hash(compressed_message) # sha 256 ΠΡΙΝ ΤΟ ENCODE
                write_Json(encoded_message_with_error,"5%",based_message, compressed_entropy) #creation of Json

                decoded_message = decode_message(encoded_message_with_error) #decoding of the

                #hashed_decoded_message = hash(decoded_message)
                page_data = [{'original': data,
                              'compressed': compressed_message,
                              'compressed_entropy':compressed_entropy,
                              'encoded': encoded_message,
                              'based64': based_message,
                              'de_based64': debased_message,
                              'error': error,
                              'received': encoded_message_with_error,
                              'decoded_message': decoded_message}
                             ]
        return render_template("results.html", data= page_data)



    @socket.on('receive_json')
    def handle_the_json(json):
        print('received json: ' + str(json))

    if __name__ == "__main__":
        socket.run(app)

    # ----------------------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------compress-------------------------------------------------------------------------------
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

        #print("During the encoding process, we choose the following generator polynomial:")
        #print("Generator Polynomial g(x):")
        #print(format_polynomial(generator_polynomial))

        # Convert the message into chunks of k bits
        chunks = [message[i:i + k] for i in range(0, len(message), k)]

        # Construct the generator matrix
        G = construct_generator_matrix(generator_polynomial, k)

        #print("\nGenerator Matrix (G):")
        for row in G:
            print(row)

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
            encoded_word = ''.join(map(str,encoded_word))
            encoded_words.append(encoded_word)
            encoded_string = ''.join(map(str, encoded_words))
            #print(f"\nMessage chunk: {chunk}")
            #print(f"Encoded word: {''.join(map(str, encoded_word))}")

        return encoded_string
    #-----------------------------------------------------------------------------------------------------------------------------
    #-------------------------------------------decode----------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------

    def decode_message(encoded_string):
        encoded_words = [encoded_string[i:i+7] for i in range(0, len(encoded_string), 7)]
        generator_polynomial = [1, 1, 0, 1]  # G(x) = x^3 + x + 1
        k = 4  # Size of each original word in bits
        n = k + len(generator_polynomial) - 1  # Size of each encoded word
        errors = 0
        original_words = []
        for encoded_word in encoded_words:
            # Extract the first k bits of the encoded word
            original_word = encoded_word[:k]
            # Check for errors using the generator polynomial
            remainder = divide_polynomials(encoded_word, generator_polynomial)
            has_error = any(remainder)
            original_wordcombined = ''.join(map(str,original_word))

            original_words.append(original_wordcombined)
            original_string = ''.join(map(str,original_words))
            #print(f"Encoded word: {''.join(map(str, encoded_word))} -> Original word: {''.join(map(str, original_word))} -> Error: {'Yes' if has_error else 'No'}")

        return original_string

    #----------------------------------------------------------------------------------------------------------------------------------
    #-------------------------------------------compress-------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------------------

    def symProb(String):
        sc = dict(Counter(String.upper()));
        return {k: v / sum(sc.values()) for k, v in sc.items()}

    def compressing(string):
        def best_partition(initial, final):
            pts = []  # points
            for i in range(initial + 1, final):
                diff = abs(sum(sv[initial:i]) - sum(sv[i:final]))
                pts.append((diff))
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
            new_index = [];
            for index in current_index:
                if (index[1] - index[0]) == 2: sc[index[0]] = sc[index[0]] + '0'; sc[index[1] - 1] = sc[index[
                                                                                                            1] - 1] + '1';

                if (index[1] - index[0]) > 2:
                    index_ptr = best_partition(index[0], index[1]) + 1;
                    new_index.append((index[0], index_ptr));
                    up(index[0], index_ptr);
                    new_index.append((index_ptr, index[1]));
                    down(index_ptr, index[1]);
                current_index = new_index
            stage = stage + 1


        # In[9]:

        dummy = []
        for i in range(0, len(sv)): dummy.append((sk[i], sc[i]));
        encoded_dictionary = OrderedDict(dummy)

        # In[10]:

        # # Compressed Message
        # In[11]:
        compressed_message = ''.join(sc)
        #print("For message:-", string, "\message is:-", compressed_message)

        # # Entropy Calculation:-
        # In[12]:

        H = 0
        for i in range(0, len(sv)): H = H + sv[i] * math.log((1 / sv[i]), 2);
        entropy = H


        # # Average Codeword Length
        # In[13]:

        L = 0
        for i in range(0, len(sc)): L = L + len(sc[i]) * sv[i];
        avg_length = L
        #print("Average Codeword length is:-", L, "bits/message")

        # # Compression
        # In[14]:

        code_efficiency = (H / L) * 100
        #print("Coding efficiency is :-", (H / L) * 100)

        def best_partition(initial, final):
            pts = []  # points
            for i in range(initial + 1, final):
                diff = abs(sum(sv[initial:i]) - sum(sv[i:final]))
                pts.append((diff))
            if pts.index(min(pts)) < initial:
                return pts.index(min(pts)) + initial;
            else:
                return pts.index(min(pts))

        def up(initial, final):
            for i in range(initial, final): sc[i] = sc[i] + '0'

        def down(initial, final):
            for i in range(initial, final): sc[i] = sc[i] + '1'

        return compressed_message, entropy

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