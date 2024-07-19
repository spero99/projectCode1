
def construct_generator_matrix(generator_polynomial, k):
    n = k + len(generator_polynomial) - 1
    G = []
    for i in range(k):
        row = [0] * i + generator_polynomial + [0] * (n - len(generator_polynomial) - i + 1)
        G.append(row[:n])
    return G

def divide_polynomials(dividend, divisor):
    remainder = dividend[:]
    for i in range(len(dividend) - len(divisor) + 1):
        if remainder[i] == 1:
            for j in range(len(divisor)):
                remainder[i + j] ^= divisor[j]
    return remainder[-(len(divisor)-1):]

def decode_message(encoded_string):
    # divide encoded string to words
    # encoded_words = [encoded_string[i:i + 7] for i in range(0, len(encoded_string), 7)]
    encoded_words = [list(map(int, encoded_string[i:i + 7])) for i in range(0, len(encoded_string), 7)]
    generator_polynomial = [1, 1, 0, 1]  # G(x) = x^3 + x + 1
    k = 4  # Size of each original word in bits
    n = k + len(generator_polynomial) - 1  # Size of each encoded word
    counter = 0
    string = ''
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
        print(f"Encoded word: {''.join(map(str, encoded_word))} -> Original word: {''.join(map(str, original_word))} -> Error: {'Yes' if has_error else 'No'}")

    for word in original_words:
        string = string + ''.join(map(str, original_word))
    original_string = str(string)
    print(original_string)
    return original_string,counter

encoded_string = "101110011100101111111111111101110011001011111111111100101111111001101011111110010111111111111111111111111011100110100010111001111111111111110111001011100111111110011010111111111111110111001111111111111111101000011100111010001101000100101111111111111111101110011111111011100101110011111111111111111111110111001111111111111111010001111111111111101000111111111111111111111111101000111111111100101011100111001001110011111111111111101110011110010110100011001011111111011100111010001111111101110001101001110010110010111111111101000101110011111111111111111111111001011111111111111110111001111111101110011111111110010111111111111111111111111111111111111111111111111111111111110010"
decoded_message = decode_message(encoded_string)
#decoded_message = decode_message(encoded_words)
print(decoded_message)

import random

def alter_bits(encoded_words, percentage):
    altered_words = []

    for encoded_word in encoded_words:
        word_length = len(encoded_word)
        num_bits_to_alter = int(word_length * percentage / 100)

        altered_word = encoded_word[:]
        indices_to_alter = random.sample(range(word_length), num_bits_to_alter)

        for index in indices_to_alter:
            altered_word[index] = 1 if altered_word[index] == 0 else 0

        altered_words.append(altered_word)
        #print(f"Original word: {''.join(map(str, encoded_word))} -> Altered word: {''.join(map(str, altered_word))} -> Altered positions: {indices_to_alter}")

    return altered_words


encoded_words = [
    [1, 0, 0, 1, 0, 1, 1],
    [0, 0, 1, 1, 0, 1, 0],
    [1, 1, 1, 0, 0, 1, 0],
    [1, 1, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 1],
    [1, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 0, 1, 0]
]  # Encoded words from ENC_3

percentage = 20  # Percentage of bits to alter
altered_words = alter_bits(encoded_words, percentage)


