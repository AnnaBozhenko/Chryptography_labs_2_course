import hashlib
from tarfile import BLOCKSIZE
import docx
import rsa
from display_keys import get_key

def get_docx_content(file_name: str):
    """function returns read content from the given file."""
    try:
        doc = docx.Document(file_name)  # Creating word reader object.
        content = '\n'.join([para.text for para in doc.paragraphs])
        return content
    except IOError:
        print("There was an error opening the file!")
        return


def get_binary_content(file_name: str):
    """function returns content of the given file in binary"""
    return open(file_name, 'rb').read()


def encode_content_sha1(file_name: str, block_size):
    """function reads binary file and returns its hashed-content (using sha1)."""
    with open(file_name, "rb") as f:
        hash_obj = hashlib.sha1()
        while True:
            data = f.read(block_size)
            if not data:
                break 
            hash_obj.update(data)
    return hash_obj


if __name__ == "__main__":
    # table of strings to cipher with different hash algorithms
    BLOCK_SIZE = 2 ** 20
    strings = ["Hello, world!", "12345", "123456", ""]
    for s in strings:
        h = hashlib.sha1(bytes(s, encoding="utf8"))
        print(f"{'String:':<15} {s} \n{'Algorithm:':<15} sha1 \n{'Hex-digest:':<15} {h.hexdigest()}\n{'Size (in bits):':<15} {h.digest_size * 8}\n")

    s = 'Боженко А. О.'
    h = hashlib.md5(bytes(s, encoding="utf8"))
    print(f"{'String:':<15} {s} \n{'Algorithm:':<15} md5 \n{'Hex-digest:':<15} {h.hexdigest()}\n{'Size (in bits):':<15} {h.digest_size * 8}\n")

    h = hashlib.sha1(bytes(s, encoding="utf8"))
    print(f"{'String:':<15} {s} \n{'Algorithm:':<15} sha1 \n{'Hex-digest:':<15} {h.hexdigest()}\n{'Size (in bits):':<15} {h.digest_size * 8}\n")

    h = hashlib.sha224(bytes(s, encoding="utf8"))
    print(f"{'String:':<15} {s} \n{'Algorithm:':<15} sha224 \n{'Hex-digest:':<15} {h.hexdigest()}\n{'Size (in bits):':<15} {h.digest_size * 8}\n")

    h = hashlib.sha256(bytes(s, encoding="utf8"))
    print(f"{'String:':<15} {s} \n{'Algorithm:':<15} sha256 \n{'Hex-digest:':<15} {h.hexdigest()}\n{'Size (in bits):':<15} {h.digest_size * 8}\n")

    h = hashlib.sha224(bytes(s, encoding="utf8"))
    print(f"{'String:':<15} {s} \n{'Algorithm:':<15} sha224 \n{'Hex-digest:':<15} {h.hexdigest()}\n{'Size (in bits):':<15} {h.digest_size * 8}\n")

    h = hashlib.sha512(bytes(s, encoding="utf8"))
    print(f"{'String:':<15} {s} \n{'Algorithm:':<15} sha512 \n{'Hex-digest:':<15} {h.hexdigest()}\n{'Size (in bits):':<15} {h.digest_size * 8}\n")

    file_n = r"pib.docx"
    s = encode_content_sha1(file_n, BLOCK_SIZE)
    s_text = get_docx_content(file_n)
    print(f"{'String:':<15} {s_text} \n{'Algorithm:':<15} sha1 \n{'Hex-digest:':<15} {s.hexdigest()}\n{'Size (in bits):':<15} {s.digest_size * 8}\n")
    
    print("\n\nTesting rsa-module functions to sign and verify digital document:")
    file_zayava = 'zayava.docx'
    KEY_SIZE = 1024
    PRIVATE_KEY_FILE = f'private_key_{KEY_SIZE}.pem'
    PUBLIC_KEY_FILE  = f'public_key_{KEY_SIZE}.pem'
    file_content = get_binary_content(file_n)
    print(f"Name of file to sign: {file_zayava}")
    hash_ = rsa.compute_hash(file_content, 'SHA-1')
    publ_key = get_key(PUBLIC_KEY_FILE, 'pb')
    priv_key = get_key(PRIVATE_KEY_FILE, 'pr')
    print(f"Private key: d = {priv_key.d}\np = {priv_key.p}\nq = {priv_key.q}")
    signature = rsa.sign(hash_, priv_key, 'SHA-1')
    print(f"Formed signature: {signature}")
    try:
        print("Verification process:")
        print(f"Given public key: {publ_key.n}\ne = {publ_key.e}") 
        print(f"Type of hash algorythm: {rsa.verify(hash_, signature, publ_key)}")
        print("Verification was successful!")
    except rsa.VerificationError:
        print("Varification failed!")

