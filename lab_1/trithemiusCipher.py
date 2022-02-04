from caesarCipher import encode


def alpha_ind(letter, alphabet):
    return alphabet.find(letter)


def is_whole(number):
    return int(number + 1) - number == 1


def comb(n):
    res = []
    i = n
    while i >= 0:
        res.append([n, i])
        if n != i:
            res.append([i, n])
        i -= 1
    return res


def encode_linear(text, alphabet, a, b):
    encoded_text = ""
    position = 0
    for letter in text:
        key = a * position + b
        encoded_text += encode(letter, alphabet, key)
        position += 1
    return encoded_text


def linear_coefficients(encoded_text, decoded_text, alphabet):
    a = None
    b = None
    position_1 = -1
    position_2 = -1
    i = 0
    for decoded_letter in encoded_text:
        if decoded_letter in alphabet:
            if position_1 == -1:
                position_1 = i
            else:
                position_2 = i
                break
        i += 1
    if position_1 != -1 and position_2 != -1:
        x_1 = alpha_ind(decoded_text[position_1], alphabet)
        x_2 = alpha_ind(decoded_text[position_2], alphabet)
        y_1 = alpha_ind(encoded_text[position_1], alphabet)
        y_2 = alpha_ind(encoded_text[position_2], alphabet)
    #     -------------
    # y_1 = (x_1 + a * position_1 + b) % N, where N is length of alphabet
    # y_2 = (x_2 + a * position_2 + b) % N
    # let index_i = (x_i + a * position_i + b)
    # so
    # y_1 = index_1 % N
    # y_2 = index_2 % N
    # y_i = index_i % N -> index_i - f_i * N = y_i,
    # where f_i is integer (sign(f_i) == sign(index_i)), that is the nearest lowest number divisible by N
    # so, in that program suppose that index_i is always positive (bug if negative is necessary)
    # f_i belongs to natural numbers with zero
    # y_1 = index_1 - f_1 * N
    # y_2 = index_2 - f_2 * N
    # so
    # index_1 = y_1 + f_1 * N
    # index_2 = y_2 + f_2 * N
    # so
    # x_1 + a * position_1 + b = y_1 + f_1 * N
    # x_2 + a * position_2 + b = y_2 + f_2 * N
    # so
    # (according to the first equation): b = y_1 + f_1 * N - x_1 - a * position_1
    # (second equation): x_2 + a * position_2 + y_1 + f_1 * N - x_1 - a * position_1 = y_2 + f_2 * N
    # a * (position_2 - position_1) = -(x_2) - (y_1) - (f_1) * N + x_1 + y_2 + f_2 * N
    # a = ( -(x_2) - (y_1) - (f_1) * N + x_1 + y_2 + f_2 * N ) / (position_2 - position_1)
    # we suppose that a and b must be positive integers
    # -----------
    #     a = ( -(x_2) - (y_1) - 0 * len(alphabet) + x_1 + y_2 + 0 * len(alphabet) ) / (position_2 - position_1)
    #     b = y_1 + 0 * len(alphabet) - x_1 - a * position_1
        i = 0
        while True:
            f = comb(i)
            for f_pair in f:
                a = ( -(x_2) - (y_1) - f_pair[0] * len(alphabet) + x_1 + y_2 + f_pair[1] * len(alphabet) ) / (position_2 - position_1)
                if a > 0 and is_whole(a):
                    b = y_1 + f_pair[0] * len(alphabet) - x_1 - a * position_1
                    if b > 0 and is_whole(b):
                        break
                else:
                    a = None
                    b = None
            if a is not None and b is not None:
                break
            i += 1

    return [a, b]


def encode_quadratic(text, alphabet, a, b, c):
    encoded_text = []
    for p in range(len(text)):
        if text[p] in alphabet:
            key = (alpha_ind(text[p], alphabet) + a * (p ** 2) + b * p + c) % len(alphabet)
            encoded_text.append(alphabet[key])
        else:
            encoded_text.append(text[p])
    return "".join(encoded_text)


def decode_quadratic(text, alphabet, a, b, c):
    decoded_text = []
    for p in range(len(text)):
        if text[p] in alphabet:
            key = (alpha_ind(text[p], alphabet) - (a * (p ** 2) + b * p + c)) % len(alphabet)
            decoded_text.append(alphabet[key])
        else:
            decoded_text.append(text[p])
    return "".join(decoded_text)


# # Linear trithemius cipher
# str_1 = "HARD AS A ROCK"
# print("Original string: " + str_1)
# A = ord("A")
# alpha = "".join([chr(x) for x in range(A, A + 26)])
# encoded = encode_linear(str_1, alpha, 5, 4)
# coefs = linear_coefficients(encoded, str_1, alpha)
# print(f"Coefficients (a and b respectively): + {coefs}")
# print("Encoded string: " + encoded)
# LJFW DA S TVOB


# Quadratic trithemius cipher encoding
# str_2 = "London is the capital of Great Britain".upper()
# A = ord("A")
# alpha = "".join([chr(x) for x in range(A, A + 26)])
# a = 2
# b = 2
# c = 2
# encoded = encode_quadratic(str_2, alpha, a, b, c)
# print(f"Encoded: {encoded}")
# print(decode_quadratic(encoded, alpha, a, b, c))
# NUBDEX SI HNG IOPYDIV OT ITKOT LZSJAWT


# Linear decoding
# A = ord("A")
# alpha = "".join([chr(x) for x in range(A, A + 26)])
# original = "encoded text".upper()
# encoded = "julclekxy sfay".upper()
# coefs = linear_coefficients(encoded, original, alpha)
# print(f"Coefficients: {coefs}")
# coefs [2,5]


# Quadratic trithemius cipher decoding (brute force)
# str = "wkil rnf cgsgoirncm".upper()
# A = ord("A")
# alpha = "".join([chr(x) for x in range(A, A + 26)])
# print("-----------")
# for a in range(1, 6):
#     for b in range(1, 6):
#         for c in range(1, 6):
#             print(f"Encoded (a={a}, b={b}, c={c}): {decode_quadratic(str, alpha, a, b, c)}")
#             print("--------")
# result: Encoded (a=1, b=2, c=3): TEXT FOR ENCRYPTION