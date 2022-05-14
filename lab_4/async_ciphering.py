import random

def inter_plains(a : int, b : int):
    """a, b - ints;
    function defines, if a and b
    are mutually plained to each other,
    i. e. their GCD is 1."""
    if (a / b == int(a / b)) or (b / a == int(b / a)):
            return False
    return True

def is_plain(a : int):
    """a - int number;
    function defines, if a is plain number"""
    if a == 1:
        return False
    divisors_numb = 0
    for i in range(1, a):
        if a / i == int(a / i):
            divisors_numb += 1
        if divisors_numb > 1:
            return False
    return True


def find_d(e_const : int, phi : int, n : int):
    """e_const, phi - constants, passed to Ferma's formula;
    phi - phi(n), passed to Ferma's formula: (e_const * d) % phi = 1
    n - number of d's to find.
    function returns number d, that satisfies Ferma's formula."""
    d_list = []
    i = 0
    while len(d_list) < n:
        i += 1
        if i == e_const:
            continue
        if (e_const * i) % phi == 1:
            log_message(f"({e_const} * {i}) mod {phi} == 1")
            d_list.append(i)
        
    log_message(f"List of possible d-values:{d_list}")
    random.seed(n % 32)
    d_index = random.randint(0, len(d_list) - 1)
    return d_list[d_index] 


def chars_to_ints(text : str):
    """test - string;
    function returns list of ascii char's numbers"""
    if text == "":
        return []
    return [ord(text[0])] + chars_to_ints(text[1:])


def ints_to_chars(coded_chars : int):
    """coded_chars - list of ints, that represent ascii encoded text.
    function returns decode string."""
    if coded_chars == []:
        return ''
    return chr(coded_chars[0]) + ints_to_chars(coded_chars[1:])


def generate_async_keys(p : int, q : int, e_const : int, d_list_len):
    """p, q, e_const - ints; d_list_len - int-number of generated d-keys. 
    function returns list of two tuples with mathematically 
    dependant keys [(key_1, n), (key_2, n)]"""
    n = p * q
    log_message(f"n = {p} * {q} = {n}")
    if p == q or n <= 90 or not (is_plain(p) and is_plain(q)):
        return []

    phi_of_n = (p - 1) * (q - 1)
    log_message(f"phi(n) = ({p} - 1) * ({q} - 1) = {phi_of_n}")
    log_message(f"e = {e_const}")
    if e_const >= phi_of_n or not inter_plains(phi_of_n, e_const):
        return []

    d_const = find_d(e_const, phi_of_n, d_list_len)
    return [(e_const, n), (d_const, n)]
    
def cipher(text, key):
    if key == []:
        return []

    log_message(f"Given key: {key}")
    ciphered_text = text[:]
    for i in range(len(ciphered_text)):
        log_message(f"Ciphered letter: ({ciphered_text[i]}^{key[0]}) mod {key[1]} = {(ciphered_text[i] ** key[0]) % key[1]}")
        ciphered_text[i] = (ciphered_text[i] ** key[0]) % key[1]
    return ciphered_text


def log_message(text):
    """text - string to be printed in terminal."""
    print(text)


if __name__ == "__main__":
    e_c = 3
    p_c = 11
    q_c = 17
    # d = 33
    # n = 123
    log_message("p = 11")
    log_message("q = 17")
    t = chars_to_ints("HELLO")
    # encoded = chars_to_ints(t)
    # print(encoded)
    keys = generate_async_keys(p_c, q_c, e_c, 1)
    log_message(f"Generated keys [public, private]: {keys}")
    encoded = cipher(t, keys[0])
    log_message(f"Ciphered: {encoded}")
    # if keys != []:
    #     print(f"[(e, n), (d, n)] : {keys}")
    #     encoded = cipher(encoded, keys[0])
    #     print(f"ciphered text: {encoded}")
    #     decoded = cipher(encoded, keys[1])
    #     print(f"deciphered text: {decoded}")
    #     print(f"deciphered as string: {ints_to_chars(decoded)}")

    # print(f"Given encoded text in ascii numbers: {t}")
    decoded = cipher(encoded, keys[1])
    print(f"Decoded in ascii numbers: {decoded}")
    print(f"Decoded text: {ints_to_chars(decoded)}")
# p = 3557,    q = 2579,    e = 3
    # p_c = 3557
    # q_c = 2579
    # e_c = 3
    # keys = generate_async_keys(p_c, q_c, e_c, 6111579)
    # log_message(f"Generated public and private keys: {keys}")
    # t_1 = [1111111]
    # log_message(f"Given number: {t_1}")
    # t_1_ciphered = cipher(t_1, keys[0])
    # log_message(f"Ciphered number: {t_1_ciphered}")
    # log_message("\nDeciphering (checking, if we get the given initial number:")
    # t_1_enciphered = cipher(t_1_ciphered, keys[1])
    # log_message(f"Enciphered {t_1_enciphered}, it's ascii symbol: {chr(t_1_enciphered[0])}")
