#!/usr/bin/python3
import re
from magicblueshell import MagicBlueShell
import time
import hashlib
import crypto
import argparse

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

    # Parse arguments
    parser = argparse.ArgumentParser(description='Sending a crafted bluetooth packet with hidden data')
    parser.add_argument('--key', help='the XOR key to use to crypt data',default='themaplecookiearmy')
    parser.add_argument('--nbbit', help='How many less significants bits we can use to hide data. Value should be between 1 and 8.', default=4)
    parser.add_argument('--message', help='The message you want to transmit, use "" to enter a string.(Example: --message "My message".', required= True)
    parser.add_argument('--basecolor', help='The base color from which we code our data, please send 3 integer between 1 and 255 and use ""("RED GREEN BLUE" FORMAT). Example: --basecolor "145 18 154".', default="255 255 255")
    args = parser.parse_args()

    # Prepare packets
    mess = crypto.str_xor_encode(args.message, crypto.hashkey(args.key))
    base_c = [ int(n) for n in args.basecolor.split()]
    bulb_commands = colorArrayToBulbCommands(encode(mess, base_c, args.nbbit))
    # Connect to the bulb
    magic = MagicBlueShell()
    mac_addr = ['f8:1d:78:63:50:78']
    magic.cmd_connect(mac_addr)

    # Send prepared packets 
    for i in bulb_commands:
        magic.cmd_send_specific_packet([i])
