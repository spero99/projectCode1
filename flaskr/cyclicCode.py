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
    G = construct_generator_matrix(generator_polynomial)  #αυτο θα χρειαστεί να το δινουμε στο j
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


def decode_message(encoded_string, generator_polynomial):
    encoded_words = [encoded_string[i:i+7] for i in range(0, len(encoded_string), 7)]
    print(encoded_words)
    k = 4  # μήκος του μηνύματος
    decoded_message = []
    for word in encoded_words:
        decoded_message.append(word[:k])  # Παίρνουμε τα πρώτα k bits ως το αρχικό μήνυμα
    return ''.join(decoded_message)

# Κύρια συνάρτηση που δέχεται το μήνυμα ως επιχείρημα
def main(message):
    # Πολυώνυμο γεννήτορας CRC-3 (x^3 + x + 1 -> '1011')
    generator_polynomial = [1, 0, 1, 1]

    # Κωδικοποίηση του μηνύματος σε λέξεις μήκους 7
    encoded_words = encode_message(message, generator_polynomial)

    # Εκτύπωση των αποτελεσμάτων
    print("Original Message: ", message)

    #θα αλλαξει για να μεινει string
    print("Encoded Words with CRC-3 (7 bits each): ")
    encoded_string= ""
    for word in encoded_words:
        print(word)
        encoded_string =encoded_string + word
    print(encoded_string)

    decoded_message = decode_message(encoded_string, generator_polynomial)
    print("Decoded Message: ", decoded_message)
    if decoded_message == message:
        print("allgood")
    else:
        print("there was a problem")

# Παράδειγμα κλήσης της συνάρτησης main με ένα αρχικό μήνυμα
initial_message = "1001001111101101010010110011"
main(initial_message)
