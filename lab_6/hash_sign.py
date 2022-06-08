#-*- coding: utf-8 -*-
from pathlib import Path
from datetime import datetime
import rsa
from hash_functions import encode_content_sha1
from display_keys import get_key, log_msg

PRIVATE_KEY_FILE = 'private_key_1024.pem'
PUBLIC_KEY_FILE  = 'public_key_1024.pem'
BLOCK_SIZE = 2**20
FILE_NAME = 'zayava.docx'

# get private and public keys 
priv_key = get_key(PRIVATE_KEY_FILE, 'pr')
publ_key = get_key(PUBLIC_KEY_FILE, 'pb')

#log_msg(f"private key: {priv_key}\npublic key: {publ_key}'\n'")

# get hash of the file
_hash = encode_content_sha1(FILE_NAME, BLOCK_SIZE).hexdigest()

log_msg(f"Generated hash: {_hash}")

# form metadata
date_str = datetime.now().date().isoformat()
file_size = Path(FILE_NAME).stat().st_size

metadata_to_encrypt = f"""file name: {FILE_NAME}
file size: {file_size}
sign date: {date_str}
file hash: {_hash}
"""
log_msg(f"Formed metadata: \n{metadata_to_encrypt}")

# generate signature with metadata and public key
M = metadata_to_encrypt.encode('utf-8')
signature = rsa.encrypt(M, priv_key)
with open(FILE_NAME + '.sgn', 'wb') as outf:
    outf.write(signature)

log_msg(f"Formed signature (in binary): {signature}")
log_msg(f"Formed signature (in hex): {signature.hex()}")

