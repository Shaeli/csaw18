import re
from scapy.all import *
from scapy.layers.bluetooth import *
import crypto

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

if __name__ == '__main__':
    f = input('Path to the file you want to decode?\n')
    key = input('What is the XOR key?\n')
    decoded = decode(extractByteArrayFromPcap(f), 4)
    decrypted = crypto.str_xor_decode(decoded, crypto.hashkey(key))
    print(decrypted)

