from math import gcd
from random import randint

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

def log_message(text):
    print(text)

def diffie_hellman_key_generate(g, p, a, b):
    """g, p - int, known to both communicators,
    a - int, known to one communicator,
    b - int, known to another communicator;
    the function finds mutaual secret key for communicators"""
    log_message(f"Chosen public keys: g - {g}, p - {p}")
    log_message(f"Chosen secret number of A-communicator: {a}")
    log_message(f"Chosen secret number of B-communicator: {b}")
    a_n = pow(g, a) % p
    b_n = pow(g, b) % p
    log_message(f"A = g^a mod p = {g}^{a} mod {p} = {a_n}")
    log_message(f"B = g^b mod p = {g}^{b} mod {p} = {b_n}")
    k_a = pow(b_n, a) % p
    k_b = pow(a_n, b) % p
    log_message(f"K calculated by A communicator: K = B^a mod p = {b_n}^{a} mod {p} = {k_a}")
    log_message(f"K calculated by B communicator: K = A^b mod p = {a_n}^{b} mod {p} = {k_b}")
    print(f"K(by A communicator) == K(by B communicator): {k_a == k_b} ")
    return k_a


def el_gamal_generate_keys(p_lower_bound, n, g_upper_bound = 10):
    """p_lower_bound, g_upper_bound, n - int;
    the function returns [private_key, secret_key], 
    where public key is tuple with three elements, 
    private key is a number"""
    # Choose p
    p_list = []
    i = p_lower_bound
    while i < n:
        if is_plain(i):
            p_list.append(i)
        i += 1
    ind_p = randint(0, n - 1)
    p = p_list[ind_p]
    log_message(f"Chosen index of p_list: {ind_p}, chosen p: {p}")
    # Choose g
    g_list = []
    i = 1
    if g_upper_bound > p - 1:
        g_upper_bound = p - 1
        if g_upper_bound < 1:
            return []
    while i < g_upper_bound:
        if is_plain(i):
            g_list.append(i)
        i += 1
    ind_g = randint(0, len(g_list) - 1)
    g = g_list[ind_g]
    log_message(f"Chosen index of g_list: {ind_g}, chosen p: {g}")
    # Choose x, let upper bound for possible x set will be g's upper bound
    x_list = list(range(1, g_upper_bound))
    ind_x = randint(0, len(x_list) - 1)
    x = x_list[ind_x]
    log_message(f"Chosen index of x_list: {ind_x}, chosen x: {x}")
    # Calculate y
    y = pow(g, x) % p
    return [(g, p, y), x]


def elgamal_cipher(secret_info, public_key, n = 5):
    """secret_info, n - int; public_key - tuple with ints - (g, p, y);
    the function cipherss secret_info and returns pair [a, b]"""
    p = public_key[0]
    g = public_key[1]
    y = public_key[2]
    log_message(f"Ciphering \nM (secret_info): {secret_info},  p: {p}, g: {g}, y: {y}")
    k_list = []
    i = 1
    while len(k_list) < n:
        if gcd(i, p - 1) == 1:
            k_list.append(i)
        i += 1
    ind_rand = randint(0, n - 1)
    k = k_list[ind_rand]
    # k = 9
    # log_message(f"Chosen k: {k}")
    log_message(f"Chosen index of k_list: {ind_rand}, chosen k: {k}")
    a = pow(g, k) % p
    log_message(f"a = g^k mod p = {g}^{k} mod {p} = {a}")
    b = (pow(y, k) * secret_info) % p
    log_message(f"b = (y^k * M) mod p = ({y}^{k} * {secret_info}) mod {p} = {b}")
    return [a, b]


def elgamal_encipher(ciphered_pair, x, p):
    """keypair - [int, int]"""
    a = ciphered_pair[0]
    b = ciphered_pair[1]
    log_message(f"given ciphered pair [a, b]: [{a}, {b}]; secret key: {x}, p: {p}")
    result = (b * pow(a, p - 1 - x)) % p
    log_message(f"(b * a^(p - 1 - x)) mod p = ({b} * {a}^({p} - 1 - {x})) mod p = {result}")
    return result

if __name__ == "__main__":
    # example 1 of diffie-hellman key exchange algorythm
    # p_val = 23
    # g_val = 5
    # a_val = 6
    # b_val = 15 
    # key = diffie_hellman_key_generate(g_val, p_val, a_val, b_val)
    # log_message(f"Generated mutaual key: {key}")

    # example 2 to diffie-hellman exchange algorythm
    # g_val = 7
    # p_val = 29
    # a_val = 10
    # b_val = 4
    # key = diffie_hellman_key_generate(g_val, p_val, a_val, b_val)
    # log_message(f"Generated common key: {key}")

    # example 1.a to elgamal cipher
    # m_val = 2035
    # p_val = 2357
    # g_val = 2
    # x_val = 1751
    # y_val = pow(g_val, x_val) % p_val
    # log_message(f"y = g^x mod p = {g_val}^{x_val} mod {p_val} = {y_val}")
    # public_key = (p_val, g_val, y_val)
    # # cipher
    # log_message(f"Let's cipher info: {m_val}")
    # ciphered = elgamal_cipher(m_val, public_key)
    # log_message(f"Ciphered info: {ciphered}")
    # # encipher
    # enciphered = elgamal_encipher(ciphered, x_val, p_val)
    # log_message(f"Enciphered info: {enciphered}")

    # example 1.b to elgamal cipher
    # m_val = 1009
    # p_val = 4153
    # g_val = 2
    # y_val = 1423
    # log_message(f"Let's cipher info: {m_val}")
    # ciphered = elgamal_cipher(m_val, (p_val, g_val, y_val))
    # log_message(f"Ciphered info: {ciphered}")

    log_message("Let's encipher with k = 11")
    enciphered1 = elgamal_encipher((2048, 405), x = 5, p = 4153)
    log_message(f"Enciphered: {enciphered1}")
    log_message("Let's encipher with k = 5")
    enciphered2 = elgamal_encipher((32, 2630), x = 5, p = 4153)
    log_message(f"Enciphered: {enciphered2}")


