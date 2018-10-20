import hashlib

def hashkey(key):
    return hashlib.sha256(key.encode('utf-8')).hexdigest()

def str_xor(msg, key):
    return "".join([chr(ord(m) ^ ord(k)) for (m,k) in zip(msg, key)])
