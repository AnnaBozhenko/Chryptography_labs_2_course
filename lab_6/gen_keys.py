import rsa

KEY_SIZE = 16
(pub_key, priv_key) = rsa.newkeys(KEY_SIZE)

with open('private_key_{}.pem'.format(KEY_SIZE), 'wb') as outf:
    outf.write(priv_key.save_pkcs1())

with open('public_key_{}.pem'.format(KEY_SIZE), 'wb') as outf:
    outf.write(pub_key.save_pkcs1())