
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

#Example usage:

encoded_words = [
    [1, 0, 0, 1, 0, 1, 1],
    [1, 0, 1, 1, 0, 1, 0],
    [0, 1, 1, 0, 0, 1, 0],
    [1, 1, 0, 1, 0, 0, 0],
    [1, 1, 0, 0, 0, 1, 1],
    [0, 0, 1, 1, 1, 0, 0],
    [1, 0, 1, 1, 0, 1, 0]
]  # Encoded words from ENC_3
decoded_message = decode_message(encoded_words)
print("\nDecoded Message: ", [''.join(map(str, word)) for word in decoded_message])