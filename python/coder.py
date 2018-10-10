import re
def encode(msg, color, nbBits):
    #msg: String
    #color: [RR,GG,BB]
    #nbBits: interger c [1,8]

    msg += '\x04'
    msgBinaryStr = ''.join('{0:08b}'.format(ord(x), 'b') for x in msg)
    payloadByteArray = []
    mask = 256 - pow(2, nbBits)

    while (len(msgBinaryStr) % nbBits != 0):
        msgBinaryStr += '0'

    i = 0
    while (len(msgBinaryStr) > 0):
        data = int(msgBinaryStr[0:nbBits], 2)
        msgBinaryStr = msgBinaryStr [nbBits:]
        if (i % 3 == 0):
            payloadByteArray.append([])
        payloadByteArray[i // 3].append((color[i % 3] & mask) + data)
        i += 1

    while (i % 3 != 0):
        payloadByteArray[i // 3].append(color[i % 3])
        i += 1

    return payloadByteArray

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

if __name__ == '__main__':
    print(decode(encode("Skynet is Alive !", [255,255,255], 4), 4))


