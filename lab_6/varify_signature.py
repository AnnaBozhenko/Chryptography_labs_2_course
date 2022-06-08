import rsa
import pprint
import re
from hash_functions import encode_content_sha1
from display_keys import get_key, log_msg

BLOCK_SIZE = 2**20
KEY_SIZE = 1024
FILE_NAME = 'zayava.docx'
PRIVATE_KEY_FILE = f'private_key_{KEY_SIZE}.pem'
# PUBLIC_KEY_FILE = 'public_key_1024.pem'
raw_file = open(FILE_NAME, 'rb').read()

# get hash of the file
_hash = encode_content_sha1(FILE_NAME, BLOCK_SIZE).hexdigest()
log_msg(f"Hash from file: {_hash}")

# get content of signature
with open(FILE_NAME + '.sgn', 'rb') as inf:
    signature = inf.read()

# get content of publ key 
priv_key = get_key(PRIVATE_KEY_FILE, 'pr')
# publ_key = get_key(PUBLIC_KEY_FILE, 'pb')

# get hash and metadata with the signature and public key
message = rsa.decrypt(signature, priv_key)
log_msg(f"Extracted metadata:")
pprint.pprint(message)
_hash_from_signature = re.findall('file hash: (.+)', message.decode('utf-8'))[0]
log_msg(f"Hash from signature: {_hash_from_signature}")
log_msg(f"Varification was successful: {_hash == _hash_from_signature}")
