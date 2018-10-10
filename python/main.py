from coder import *
from pcap import *

def exctractPayloadFromPcap(pcap, nbBits):
    colorsByteArray = extractByteArrayFromPcap(pcap)
    payload = decode(colorsByteArray, nbBits)
    return payload

print(exctractPayloadFromPcap('white.pcap', 4))