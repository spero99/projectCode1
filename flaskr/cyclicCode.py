
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

    print("During the encoding process, we choose the following generator polynomial:")
    print("Generator Polynomial g(x):")
    print(format_polynomial(generator_polynomial))

    # Convert the message into chunks of k bits
    chunks = [message[i:i+k] for i in range(0, len(message), k)]

    # Construct the generator matrix
    G = construct_generator_matrix(generator_polynomial, k)

    print("\nGenerator Matrix (G):")
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
        encoded_words.append(encoded_word)
        print(f"\nMessage chunk: {chunk}")
        print(f"Encoded word: {''.join(map(str, encoded_word))}")

    return encoded_words

# Example usage:
message = "1001001111101101010010110011"  # Original message
encoded_words = encode_message(message)

# Print the list of encoded words
print("\nList of Encoded Words:")
for word in encoded_words:
    print(''.join(map(str, word)))