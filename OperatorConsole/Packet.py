#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Module for managing data packets. Useful for sending data to a
microcontroller over a serial connection. This module adds control characters
and a checksum to a list of integers. It returns the new list.

Packet structure: Each packet consists of a start and end char, data
ints, and a checksum int. For example:
Start,Data1,Data2,Data3,Checksum,End

@author:Kristian Charboneau
"""


class Packet:
    """
    """
    def __init__(self):
        pass

    def to_packet(self, values):
        """
        Adds control chars and checksum int to a list of ints
        """
        checksum = 0
        for i in values:  # calculate checksum
            checksum = checksum ^ i
        values.insert(0, '<')
        values.append(checksum)
        values.append('>')

        return(values)

    def to_list(self, values):
        """
        Strips the control characters and checksum from a list of intergers.
        """
        values.remove('>')
        values.remove('<')
        values.pop()
        return values

    def validate(self, values):
        """
        Validates a packetized string. Returns 1 for success and 0 for failure.
        """
        values.remove('>')
        values.remove('<')
        packet_checksum = values.pop()

        checksum = 0
        for i in values:  # calculate checksum
            checksum = checksum ^ i

        if checksum == packet_checksum:
            return True
        else:
            return False

    def gen_checksum(self, packet):
        """
        Generate a checksum of a packet. The method used is a simple XOR
        method.
        """
        checksum = 0
        for i in packet:  # calculate checksum
            checksum = checksum ^ i
        return checksum

if __name__ == '__main__':
    p = Packet()
    l = [1, 2, 0, 65, 66, 254]

    print("Packet:%s" % p.to_packet(l))
