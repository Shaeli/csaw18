import hashlib
import base64
import codecs

def hashkey(key, qrcode=False):
    if qrcode:
        return key.encode()
    else:
        h = hashlib.sha256(key.encode('utf-8')).hexdigest()
        return codecs.decode(h, "hex")

def str_xor_encode(msg, key):
    encoded = ""
    for i in range(0, len(msg)):
        encoded += chr(ord(msg[i]) ^ key[i % len(key)])
    return base64.b64encode(encoded.encode('iso-8859-1'))

def str_xor_decode(b64msg, key):
    msg = base64.b64decode(b64msg).decode('iso-8859-1')
    decoded = ""
    for i in range(0, len(msg)):
        decoded += chr(ord(msg[i]) ^ key[i % len(key)])
    return decoded
