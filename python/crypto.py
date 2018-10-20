import hashlib
import base64
import codecs

def hashkey(key):
    h = hashlib.sha256(key.encode('utf-8')).hexdigest()
    return codecs.decode(h,"hex")

def str_xor_encode(msg, key):
    encoded = "".join([chr(ord(m) ^ k) for (m,k) in zip(msg, key)])
    return base64.b64encode(encoded.encode())

def str_xor_decode(b64msg, key):
    msg = base64.b64decode(b64msg).decode()
    return "".join([chr(ord(m) ^ k) for (m,k) in zip(msg, key)])
