import rsa

def log_msg(text:str):
    print(text)


def get_key(file_name: str, key_type: str):
    with open(file_name, 'rb') as inf:
        key_pem = inf.read()
        if key_type == 'pr':
            return rsa.PrivateKey.load_pkcs1(key_pem)
        else:
            return rsa.PublicKey.load_pkcs1(key_pem)

if __name__ == "__main__":
    KEY_SIZE = 1024
    PRIVATE_KEY_FILE = f'private_key_{KEY_SIZE}.pem'
    PUBLIC_KEY_FILE  = f'public_key_{KEY_SIZE}.pem'
    priv_key = get_key(PRIVATE_KEY_FILE, 'pr')
    log_msg("Private key:\nn= {} \nd= {} \ne= {} \np= {} \nq= {}".format(priv_key.n, priv_key.d, priv_key.e, priv_key.p, priv_key.q))
    publ_key = get_key(PUBLIC_KEY_FILE, 'pb')
    log_msg("Public key:\nn={} \ne={}".format(publ_key.n, publ_key.e))
