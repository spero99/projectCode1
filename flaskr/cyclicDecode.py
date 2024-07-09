
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
    encoded_words = [encoded_string[i:i + 7] for i in range(0, len(encoded_string), 7)]
    generator_polynomial = [1, 1, 0, 1]  # G(x) = x^3 + x + 1
    k = 4  # Size of each original word in bits
    n = k + len(generator_polynomial) - 1  # Size of each encoded word
    errors = 0
    original_string = ""
    original_words = []
    for encoded_word in encoded_words:
        # Extract the first k bits of the encoded word
        original_word = encoded_word[:k]
        # Check for errors using the generator polynomial
        remainder = divide_polynomials(encoded_word, generator_polynomial)
        has_error = any(remainder)
        original_word = ''.join(map(str, original_word))
        original_words.append(original_word)
        original_string = ''.join(map(str, original_words))



    return original_string


#Example usage:

encoded_words = "1011100111001011111111111111011100110010111111111111001011111110011010111111100101111111111111111111111110111001101000101110011111111111111101110010111001111111100110101111111111111101110011111111111111111010000111001110100011010001001011111111111111111011100111111110111001011100111111111111111111111101110011111111111111110100011111111111111010001111111111111111111111111010001111111111001010111001110010011100111111111111111011100111100101101000110010111111110111001110100011111111011100011010011100101100101111111111010001011100111111111111111111111110010111111111111111101110011111111011100111111111100101111111111111111111111111111111111111111111111111111111111100100000000"

decoded_message = decode_message(encoded_words)
print(decoded_message)
if decoded_message=="1011111011111111011110011111111011110011111100101111111111110111101001111111111101110111111100111111111101111111111111010111110111011001111111111011111110111011111111111111101111111111110111111111010011111111111111011111111010111110011111111111011111101101110011110111110111111011011011101100111111011011111111111111110011111111101111111011111111101111111111111111111111111111111111100":
    print("ok")