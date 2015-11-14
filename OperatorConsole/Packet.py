#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Module for managing data packets. Useful for sending data to a
microcontroller over a serial connection. This module can convert a list of
integers into a string of bytes, convert a string of bytes into a list, and
validate the checksum of a packet. The range of allowed numbers is 0-254 (255
is reserved as the Start and End value). While this is limited, it should be
sufficient for simple communication needs.

Packet structure: Each packet consists of a start and end byte, mode byte, data
bytes, and checksum byte. For example:
Start,Mode,Data1,Data2,Data3,Checksum,End

@author:Kristian Charboneau
"""


class Packet:
    """
    """
    def __init__(self):
        pass

    def to_packet(self, input):
        """
        Converts a list to a packetized string.
        Returns a string, or 0 if there was a failure.
        """
        input = bytearray(input)
        packet = 0
        for i in input:
            if i < 0 or i > 254:
                return 0
            else:
                print("i%s" % i)
                # print str(l)
                try:
                    packet += i
                except:
                    pass
            print("Packet:%d" % packet.decode("utf-8"))

        return(packet)

    def to_list(self, string):
        """
        Converts a packetized string to a list.
        """
        pass

    def validate(self, string):
        """
        Validates a packetized string. Returns 1 for success and 0 for failure.
        """
        pass

    def gen_checksum(self, packet):
        """
        Generate a checksum of a packet. The method used is a simple XOR
        method. Code from "http://stackoverflow.com/questions/26517869/creating
        -xor-checksum-of-all-bytes-in-hex-string-in-python"
        """
        checksum = 0
        for el in packet:
            checksum ^= ord(el)

if __name__ == '__main__':
    p = Packet()
    l = [1, 2, 0, 65, 66, 254]

    print("Packet:%s" % p.to_packet(l))
