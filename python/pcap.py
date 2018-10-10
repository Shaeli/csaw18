import re
from scapy.all import *

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
    print(extractByteArrayFromPcap('white.pcap'))
