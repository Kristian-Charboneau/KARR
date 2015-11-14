#! /usr/bin/env python
"""Module for interfacing with KARR's propeller chip
@author:Kristian Charboneau
"""
import serial


def move_x(value):
    pass


def move_y(value):
    pass


def move_z(value):
    pass


def rot_x(value):
    pass


def rot_y(value):
    pass


def rot_z(value):
    pass


def _light(value):
    pass


def camera_pan(value):
        pass


def camera_tilt(value):
        pass


def depth():
    pass


class Light():

    def __init__(self):
        self.brightness = 0

    def set_brightness(self, value):
        self.brightness = value

    def get_brightness(self):
        return self.brightness


def cycle():
    """ Send and receive data with the propeller chip. Should be called every
    time the mainloop starts over
    """
    pass
