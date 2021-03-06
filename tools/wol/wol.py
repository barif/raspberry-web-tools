#!/usr/bin/env python

import struct, socket

def WakeOnLan(ethernet_address):
    addr_byte = ethernet_address.split(':')
    hw_addr = struct.pack('BBBBBB', int(addr_byte[0], 16),
                          int(addr_byte[1], 16),
                          int(addr_byte[2], 16),
                          int(addr_byte[3], 16),
                          int(addr_byte[4], 16),
                          int(addr_byte[5], 16))

    # Build the Wake-On-LAN "Magic Packet"...
    msg = '\xff' * 6 + hw_addr * 16

    # ...and send it to the broadcast address using UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(msg, ('<broadcast>', 9))
    s.close()
    return 0

def main():
    import sys
    try:
        if ':' in sys.argv[1]:
            WakeOnLan(sys.argv[1])
    except IndexError:
        print '''Usage:
python''', sys.argv[0], '<MAC ADDRESS>'
    return 0

if __name__ == '__main__': main()