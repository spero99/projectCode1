
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

def decode_message(encoded_words):
    generator_polynomial = [1, 1, 0, 1]  # G(x) = x^3 + x + 1
    k = 4  # Size of each original word in bits
    n = k + len(generator_polynomial) - 1  # Size of each encoded word

    original_words = []
    for encoded_word in encoded_words:
        # Extract the first k bits of the encoded word
        original_word = encoded_word[:k]
        # Check for errors using the generator polynomial
        remainder = divide_polynomials(encoded_word, generator_polynomial)
        has_error = any(remainder)
        original_words.append(original_word)
        print(f"Encoded word: {''.join(map(str, encoded_word))} -> Original word: {''.join(map(str, original_word))} -> Error: {'Yes' if has_error else 'No'}")

    return original_words


encoded_words = [
    [1, 0, 0, 1, 0, 1, 1],
    [0, 0, 1, 1, 0, 1, 0],
    [1, 1, 1, 0, 0, 1, 0],
    [1, 1, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 1],
    [1, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 0, 1, 0]
]  # Encoded words from ENC_3

decoded_message = decode_message(encoded_words)
print("\nDecoded Message: ", [''.join(map(str, word)) for word in decoded_message])

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

        altered_words.append((altered_word, indices_to_alter))
        print(f"Original word: {''.join(map(str, encoded_word))} -> Altered word: {''.join(map(str, altered_word))} -> Altered positions: {indices_to_alter}")

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

encoded_string = ""
for word in encoded_words:
    encoded_string = encoded_string + ''.join(map(str, word))
print(encoded_string)


encoded_words2 = [encoded_string[i:i + 7] for i in range(0, len(encoded_string), 7)]
print(encoded_words2)
percentage = 20  # Percentage of bits to alter
altered_words = alter_bits(encoded_words, percentage)

#print("\nList of Altered Words with Altered Positions:")
#for word, altered_positions in altered_words:
 #   print(f"Altered word: {''.join(map(str, word))}, Altered positions: {altered_positions}")

print("DECODED WITH ERRORS")
decoded2 = decode_message(altered_words)