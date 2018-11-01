#!/usr/bin/python3
import re
from scapy.all import *
from scapy.layers.bluetooth import *
import crypto
import argparse

def decode(byteArray, nbBits):
    # byteArray: [[RR,GG,BB],...]
    # nbBits: interger c [1,8]

    mask = 256 - pow(2, nbBits)
    mask = 255 - mask
    bin_text = ""
    for i in range(0, len(byteArray)):
        for j in range(3):
            current_bin = "{0:b}".format((mask & byteArray[i][j]))
            while len(current_bin) != 4:
                current_bin = "0" + current_bin
            bin_text = bin_text + current_bin
    result = "".join(chr(int(bin_text[i:i+8], 2)) for i in range(0, len(bin_text),8))
    str = re.match("(.*)\\x04",result)

    return str.group(1) if str else result

def extractByteArrayFromPcap(pcap):
    packets = rdpcap(pcap)
    byteArray = []
    for pkt in packets:
        if pkt.haslayer('Write Request'):
            color = re.search(b'\x56(.)(.)(.)\x00\xf0\xaa', pkt['Write Request'].data)
            if color:
                byteArray.append([
                    int.from_bytes(color.group(1), 'big'),
                    int.from_bytes(color.group(2), 'big'),
                    int.from_bytes(color.group(3), 'big')])

    return byteArray
def check_correct_nb_bit(value):
    value = int(value)
    if value < 1 or value > 8:
        raise argparse.ArgumentTypeError('nbbit value is: {} and should be between 1 and 8'.format(value))
    return value

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Decoding a bluetooth hidden message')
    parser.add_argument('--file', help='The file that contains the bluetooth trafic capture', required=True)
    parser.add_argument('--key', help='The XOR key used to crypt data', default='themaplecookiearmy')
    parser.add_argument('--nbbit', help='How many less significants bits we used to hide data. Value between 1 and 8.', default=4, type=check_correct_nb_bit)
    args = parser.parse_args()
    decoded = decode(extractByteArrayFromPcap(args.file), args.nbbit)
    decrypted = crypto.str_xor_decode(decoded, crypto.hashkey(args.key))
    print(decrypted)

