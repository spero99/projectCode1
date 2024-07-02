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
                compressed_message = compressed_data[1]
                compressed_entropy = compressed_data[2]
                encoded_message = encode_message(compressed_message) #encoding of the data
                encoded_message_with_error = simulateError(encoded_message) #simulation of errors by noise during transmission
                hashed_message = hash(encoded_message_with_error)
                write_Json(encoded_message_with_error,"5%",hashed_message, compressed_entropy) #creation of Json
                decoded_message = decode_message(encoded_message_with_error) #decoding of the

        return


    @socket.on('message')
    def handle_message(msg):
        socket.send("test")


    @socket.on('receive_file')
    def handle_file(file):
        socket.send("testfile")

    @socket.on('receive_json')
    def handle_the_json(json):
        print('received json: ' + str(json))

    if __name__ == "__main__":
        socket.run(app)

    # ----------------------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------compress-------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------------------
    def construct_generator_matrix(generator_polynomial):
        k = 4  # μήκος του μηνύματος
        n = len(generator_polynomial) + k - 1  # μήκος της κωδικοποιημένης λέξης

        # Κατασκευή της μήτρας γεννήτορας
        G = [[0] * n for _ in range(k)]
        for i in range(k):
            for j in range(len(generator_polynomial)):
                G[i][i + j] = generator_polynomial[j]

        return G

    def multiply_matrices(message_vector, G):
        codeword = [0] * len(G[0])
        for i in range(len(message_vector)):
            if message_vector[i] == 1:
                for j in range(len(G[i])):
                    codeword[j] = (codeword[j] + G[i][j]) % 2
        return codeword

    def encode_message(message, generator_polynomial):
        G = construct_generator_matrix(generator_polynomial)  # αυτο θα χρειαστεί να το δινουμε στο j
        k = len(G)  # Αριθμός γραμμών στη μήτρα G
        encoded_words = []
        for i in range(0, len(message), k):
            chunk = message[i:i + k]
            if len(chunk) < k:
                chunk = chunk.ljust(k, '0')  # pad with zeros if needed
            message_vector = [int(bit) for bit in chunk]
            codeword = multiply_matrices(message_vector, G)
            encoded_words.append(''.join(map(str, codeword)))
        return encoded_words

    def decode_message(encoded_string):
        generator_polynomial = [1, 0, 1, 1]
        encoded_words = [encoded_string[i:i + 7] for i in range(0, len(encoded_string), 7)]
        #print(encoded_words)
        k = 4  # μήκος του μηνύματος
        decoded_message = []
        for word in encoded_words:
            decoded_message.append(word[:k])  # Παίρνουμε τα πρώτα k bits ως το αρχικό μήνυμα
        return ''.join(decoded_message)

    # Κύρια συνάρτηση που δέχεται το μήνυμα ως επιχείρημα
    def encode_message(message):
        # Πολυώνυμο γεννήτορας CRC-3 (x^3 + x + 1 -> '1011')
        generator_polynomial = [1, 0, 1, 1]

        # Κωδικοποίηση του μηνύματος σε λέξεις μήκους 7
        encoded_words = encode_message(message, generator_polynomial)
         #print("Encoded Words with CRC-3 (7 bits each): ")
        encoded_string = ""
        for word in encoded_words:
            encoded_string = encoded_string + word

        return encoded_string

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

        return compressed_message, entropy, avg_length

    def simulateError(encoded_string):
        string_length = len(encoded_string)
        changed_bits = string_length * 5 // 100 # 5% error on sent simulation
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