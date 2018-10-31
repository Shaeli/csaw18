import re
from magicblueshell import MagicBlueShell
import time
import hashlib
import crypto

def encode(msg, color, nbBits):
    #msg: String
    #color: [RR,GG,BB]
    #nbBits: interger c [1,8]

    msg = msg.decode('utf-8') + '\x04'
    msgBinaryStr = ''.join('{0:08b}'.format(ord(x), 'b') for x in msg)
    colorsArray = []
    mask = 256 - pow(2, nbBits)

    while (len(msgBinaryStr) % nbBits != 0):
        msgBinaryStr += '0'

    i = 0
    while (len(msgBinaryStr) > 0):
        data = int(msgBinaryStr[0:nbBits], 2)
        msgBinaryStr = msgBinaryStr [nbBits:]
        if (i % 3 == 0):
            colorsArray.append([])
        colorsArray[i // 3].append((color[i % 3] & mask) + data)
        i += 1

    while (i % 3 != 0):
        colorsArray[i // 3].append(color[i % 3])
        i += 1

    return colorsArray

def colorArrayToBulbCommands(colorsArray):
    commands = []
    for color in colorsArray:
        red = "%x" % color[0]
        green = "%x" % color[1]
        blue = "%x" % color[2]
        commands.append("56" + red + green + blue + "00f0aa")
    return commands

if __name__ == '__main__':
    key = input('please enter your XOR key\n')
    message = input('please enter the message that you need to send\n')
    mess = crypto.str_xor_encode(message, crypto.hashkey(key))
    base_color = input('please enter the base color (example: "255 255 255"for white)\n')
    base_c = [ int(n) for n in base_color.split()]
    bulb_commands = colorArrayToBulbCommands(encode(mess, base_c, 4))
    magic = MagicBlueShell()
    mac_addr = ['f8:1d:78:63:50:78']
    magic.cmd_connect(mac_addr)
    for i in bulb_commands:
        magic.cmd_send_specific_packet([i])
        #time.sleep(1) After some tests, it looks like it's not necessary... w/s
    #Eleonore's tests
    """
    for i in range(40):
        magic.cmd_send_specific_packet(['56ff000000f0aa'])
        magic.cmd_send_specific_packet(['5600ff0000f0aa'])
        magic.cmd_send_specific_packet(['560000ff00f0aa'])"""

