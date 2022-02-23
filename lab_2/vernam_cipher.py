import random

ENCODING = 'CP866'

def key_in_bytes(rand_seed, text):
  seed = random.seed(rand_seed)
  return bytes(random.randint(0, 255) for char in text)


def string_repres_of_bytes(byte_object):
  return ' '.join(["{0:08b}".format(x) for x in byte_object])
 

def encode_vernam(text, rand_seed, encoding_f, logging = True):
  bytes_text = text.encode(encoding_f)
  bytes_key = key_in_bytes(rand_seed, text)
  bytes_ciphered_text = bytes(i ^ j for i, j in zip(bytes_text, bytes_key))
  if (logging):
    print(f"str_bytes_text = {string_repres_of_bytes(bytes_text)}")
    print(f"str_bytes_key = {string_repres_of_bytes(bytes_key)}")
    print(f"str_bytes_ciphered_text = {string_repres_of_bytes(bytes_ciphered_text)}")
  return [bytes_ciphered_text, bytes_key]


def decode_vernam(ciphered_text, cipher_key, encoding_f, logging = True):
  decoded_text = bytes(i ^ j for i, j in zip(ciphered_text, cipher_key))
  if (logging):
    print(f"str_bytes_deciphered_text: {string_repres_of_bytes(decoded_text)}")
  return decoded_text.decode(encoding_f)
  

def str_bytes_to_bytes(str):
  return bytes(int(i, 2) for i in str.split())


# Enciphering
# -----------
# message = "HIGHHOPES"
# ciphered = encode_vernam(message, 3, ENCODING)
# ciphered_t = ciphered[0]
# key = ciphered[1]
# deciphered = decode_vernam(ciphered_t, key, ENCODING)
# print(f"deciphered: {deciphered}")


# Deciphering
# -----------
key_str = "1111001 1000010 10111101 11110010 100001 110 11110000 10000100 1110111"
enciphered_str = "110001 1011 11111010 10111010 1101001 1001001 10100000 11000001 100100"
key = str_bytes_to_bytes(key_str)
enciph = str_bytes_to_bytes(enciphered_str)
enciphered = decode_vernam(enciph, key, ENCODING)
print(enciphered)
