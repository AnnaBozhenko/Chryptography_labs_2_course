#-*- coding: utf-8 -*-
from pathlib import Path
from datetime import datetime
from hash_functions import encode_content_sha1
from display_keys import get_key, log_msg

PRIVATE_KEY_FILE = 'private_key_1024.pem'
PUBLIC_KEY_FILE  = 'public_key_1024.pem'
BLOCK_SIZE = 2**20
SHA1_DIGEST_SIZE = 20
FILE_NAME = 'zayava.docx'

def encrypt_rsa(bi_message: bytes, private_key, l: int):
    k = private_key.d
    n = private_key.n
    cipher_int = int.from_bytes(bi_message, byteorder = "big")
    cipher = pow(cipher_int, k, n)
    cipher_bytes = cipher.to_bytes(l, byteorder = "big")
    return cipher_bytes

# get private and public keys 
priv_key = get_key(PRIVATE_KEY_FILE, 'pr')

#log_msg(f"private key: {priv_key}\npublic key: {publ_key}'\n'")

# get hash of the file
hashed_data = encode_content_sha1(FILE_NAME, BLOCK_SIZE).digest()

log_msg(f"Generated hash: {hashed_data}")

# form metadata
date_str = datetime.now().date().isoformat()
file_size = Path(FILE_NAME).stat().st_size

metadata_to_encrypt = f"""file name: {FILE_NAME}
file size: {file_size}
sign date: {date_str}
file hash: """

log_msg(f"Formed metadata: \n{metadata_to_encrypt}{hashed_data}")

# generate signature with metadata and public key
M = metadata_to_encrypt.encode(encoding="utf8") + hashed_data
signature = encrypt_rsa(M, priv_key, SHA1_DIGEST_SIZE * 8)
with open(FILE_NAME + '.sgn', 'wb') as outf:
    outf.write(signature)

log_msg(f"Formed signature (in binary): {signature}")
log_msg(f"Formed signature (in hex): {signature.hex()}")

