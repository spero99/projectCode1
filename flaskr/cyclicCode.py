

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
    return remainder[-(len(divisor)-1):]

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
    chunks = [message[i:i+k] for i in range(0, len(message), k)]

    # Construct the generator matrix
    G = construct_generator_matrix(generator_polynomial, k)



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


# Example usage:
message = "101111101111111101111001111111101111001111110010111111111111011110100111111111110111011111110011111111110111111111111101011111011101100111111111101111111011101111111111111110111111111111011111111101001111111111111101111111101011111001111111111101111110110111001111011111011111101101101110110011111101101111111111111111001111111110111111101111111110111111111111111111111111111111111110"  # Original message
encoded_words = encode_message(message)
print(encoded_words)

#1001011001101011100101101000010001110111000011010



#101110011100101111111111111101110011001011111111111100101111111001101011111110010111111111111111111111111011100110100010111001111111111111110111001011100111111110011010111111111111110111001111111111111111101000011100111010001101000100101111111111111111101110011111111011100101110011111111111111111111110111001111111111111111010001111111111111101000111111111111111111111111101000111111111100101011100111001001110011111111111111101110011110010110100011001011111111011100111010001111111101110001101001110010110010111111111101000101110011111111111111111111111001011111111111111110111001111111101110011111111110010111111111111111111111111111111111111111111111111111111111110010


