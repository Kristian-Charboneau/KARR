#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Module for managing data packets. Useful for sending data to a
microcontroller over a serial connection. This module adds control characters
and to a pin and value pair. It returns .

Packet structure: Each packet consists of a start and end char, pin
byte, and a value byte. For example:

Start pin value End

The start and end chars are '<' and '>'.
A possible packet could look like this (decimal representation):

60 2 100 62


@author:Kristian Charboneau
"""


class Packet:
    """
    Packet operations for communication with a microcontroller.
    """
    def __init__(self):
        pass

    def to_packet(self, pin, value):
        """
        Adds control chars to pin and value
        Returns a string.
        """
        packet = ""
        packet += "<"
        packet += str(pin)
        packet += str(value)
        packet += ">"

        return(packet)

    def to_values(self, packet):
        """
        Strips the control characters from a packet.
        Returns the pin and value integers
        """
        pin = packet[1]
        value = packet[2]
        return pin, value

    def validate(self, values):
        """
        Validates a packetized string. Not applicable for this implementation
        """
        pass

    def gen_checksum(self, packet):
        """
        Generate a checksum of a packet. The method used is a simple XOR
        method. Not applicable to current implementation.
        """
        pass

if __name__ == '__main__':
    p = Packet()
    pin = 2
    value = 100

    # bytes = str.encode(p.to_packet(pin, value))
    print()
    print("Here are the bytes in the packet:")
    for c in p.to_packet(pin, value):
        print(ord(c))
    # print("Packet:{}".format(p.to_packet(pin, value)))
