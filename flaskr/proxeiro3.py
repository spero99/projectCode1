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
    encoded_words = [list(map(str, encoded_string[i:i + 7])) for i in range(0, len(encoded_string), 7)]
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
    print(len(original_string))
    return original_string,counter

encoded_string = "1011100111001011111111111111011100110010111111111111001011111110011010111111100101111111111111111111111110111001101000101110011111111111111101110010111001111111100110101111111111111101110011111111111111111010000111001110100011010001001011111111111111111011100111111110111001011100111111111111111111111101110011111111111111110100011111111111111010001111111111111111111111111010001111111111001010111001110010011100111111111111111011100111100101101000110010111111110111001110100011111111011100011010011100101100101111111111010001011100111111111111111111111110010111111111111111101110011111111011100111111111100101111111111111111111111111111111111111111111111111111111111100100000000"
decoded_message = decode_message(encoded_string)
#print("\nDecoded Message: ", [''.join(map(str, word)) for word in decoded_message])
print(decoded_message)