import re
from scapy.all import *

packets = rdpcap('white.pcap')

payloadByteArray = []

for pkt in packets:
    if pkt.haslayer('Write Request'):
        pkt.show()
        color = re.search(b'\x56(.)(.)(.)\x00\xf0\xaa', pkt['Write Request'].data)
        payloadByteArray.append([
            int.from_bytes(color.group(1), 'big'),
            int.from_bytes(color.group(2), 'big'),
            int.from_bytes(color.group(3), 'big')])

for i in range(0, len(payloadByteArray)):
    print("{}: {} {} {}".format(i, payloadByteArray[i][0], payloadByteArray[i][1],payloadByteArray[i][2]))