import re
from scapy.all import *

packets = rdpcap('lol.pcapng')

payloadByteArray = []

for pkt in packets:
    if pkt.haslayer('Write Request'):
        pkt.show()
        color = re.search(b'\x56(.)(.)(.)\x00\xf0\xaa', pkt['Write Request'].data)
        payloadByteArray.append([color.group(1),color.group(2),color.group(3)])

for i in range(0, len(payloadByteArray)):
    print("{}: {} {} {}".format(i, payloadByteArray[i][0], payloadByteArray[i][1],payloadByteArray[i][2]))