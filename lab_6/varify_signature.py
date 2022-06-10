from distutils.filelist import findall
from hash_functions import encode_content_sha1
from display_keys import get_key, log_msg

BLOCK_SIZE = 2**20
KEY_SIZE = 1024
FILE_NAME = 'zayava.docx'
PUBLIC_KEY_FILE = 'public_key_1024.pem'
SHA1_BIT_LENGTH = 20 * 8
raw_file = open(FILE_NAME, 'rb').read()


def decrypt_rsa(cipher, public_key, l: int):
    k = public_key.e
    n = public_key.n
    cipher_int = int.from_bytes(cipher, byteorder = "big")
    message_int = pow(cipher_int, k, n)
    bi_message = message_int.to_bytes(l, byteorder = "big")
    return bi_message

# get hash of the file
hashed_data = encode_content_sha1(FILE_NAME, BLOCK_SIZE).digest()

# get content of signature
with open(FILE_NAME + '.sgn', 'rb') as inf:
    signature = inf.read()

# get content of publ key 
publ_key = get_key(PUBLIC_KEY_FILE, 'pb')

# get hash and metadata with the signature and public key
M = decrypt_rsa(signature, publ_key, SHA1_BIT_LENGTH)
log_msg(f"Extracted metadata: \n{M[:-20].decode(encoding='utf8')}{M[-20:]}")


# hash_from_signature = metadata_and_hash[-20:]
pattern = b'file hash: '
start_index = M.find(pattern) + len(pattern)
# extract 20 following bytes, which hash occupies
hash_from_signature = M[start_index : start_index + 20]
log_msg(f"Hash from file: {hashed_data}")
log_msg(f"Hash from signature: {hash_from_signature}")
log_msg(f"Varification was successful: {hashed_data == hash_from_signature}")
