#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Module for reading input from the user.
This implementation is designed to be used with a gamepad.
Each button, hat, and joystick has it's own method
@author:Kristian Charboneau
"""
import pygame

pygame.init()


button_map = {
    'X': 0,
    'Y': 3,
    'A': 1,
    'B': 2,
    'R1': 5,
    'L1': 4,
    'R2': 7,
    'L2': 6,
    'R3': 11,
    'L3': 10,
    'Start': 9,
    'Back': 8,
    'RightX': 2,
    'LeftX': 0,
    'RightY': 3,
    'LeftY': 1,
}


class Gamepad:
    """Uses Pygame to access a gamepad. Each button is presented as a method.
    range_min and range_max specify the minumin and maximum values to return
    for analog inputs. buttons return a 1 or 0. Note: for speed purposes the
    range for analog inputs is hardcoded as -100 to 100, but the range
    parameters are left for future use. At init checks if a gamepad is present,
    if no gamepad is detected, returns 0.
    """
    def __init__(self, range_min=-100, range_max=100):
        self.min = range_min
        self.max = range_max
        self.gp = pygame.joystick.Joystick(0)
        self.gp.init()
        # print(self.gp.get_id())
        # print(self.gp.get_init())
        # print(self.gp.get_numaxes())
        # print(self.gp.get_numbuttons())
        print("init!")

    def convert(self, value):
        """
        converts value from the default analog range to a new range.
        The new range is currently hardcoded as -100 to 100 and the input is
        excpected to be -1 to 1.
        """
        return value*100

        # OldRange = (OldMax - OldMin)
        # NewRange = (max - min)
        # NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + min

    def update(self):
        """
        force pygame to read input from the gamepad
        """
        pygame.event.pump()

    def get_x(self):
        """
        return value of X button
        """
        self.update()
        # pygame.event.pump()
        return(self.gp.get_button(button_map['X']))

    def get_y(self):
        """
        return value of Y button
        """
        self.update()
        return(self.gp.get_button(button_map['Y']))

    def get_a(self):
        """
        return value of A button
        """
        self.update
        return(self.gp.get_button(button_map['A']))

    def get_b(self):
        """
        return value of B button
        """
        self.update
        return(self.gp.get_button(button_map['B']))

    def get_dpad_up(self):
        """
        return value of Dpad up button
        """
        self.update
        value = self.gp.get_hat(0)
        if value[1] == 0 or -1:
            return(0)
        else:
            return(1)

    def get_dpad_down(self):
        """
        return value of Dpad up button
        """
        self.update
        value = self.gp.get_hat(0)
        if value[1] == 0 or 1:
            return(0)
        else:
            return(1)

    def get_dpad_left(self):
        """
        return value of Dpad up button
        """
        self.update
        value = self.gp.get_hat(0)
        if value[0] == 0 or 1:
            return(0)
        else:
            return(1)

    def get_dpad_right(self):
        """
        return value of Dpad up button
        """
        self.update
        value = self.gp.get_hat(0)
        if value[0] == 0 or -1:
            return(0)
        else:
            return(1)

    def get_start(self):
        """
        return value of Start button
        """
        self.update
        return(self.gp.get_button(button_map['Start']))

    def get_back(self):
        """
        return value of Back button
        """
        self.update
        return(self.gp.get_button(button_map['Back']))

    def get_r1(self):
        """
        return value of R1 button
        """
        self.update
        return(self.gp.get_button(button_map['R1']))

    def get_l1(self):
        """
        return value of L1 button
        """
        self.update
        return(self.gp.get_button(button_map['L1']))

    def get_r2(self):
        """
        return value of R2 button
        """
        self.update
        return(self.gp.get_button(button_map['R2']))

    def get_l2(self):
        """
        return value of L2 button
        """
        self.update
        return(self.gp.get_button(button_map['L2']))

    def get_r3(self):
        """
        return value of R3 button
        """
        self.update
        return(self.gp.get_button(button_map['R3']))

    def get_l3(self):
        """
        return value of L3 button
        """
        self.update
        return(self.gp.get_button(button_map['L3']))

    def get_rx(self):
        """
        return value of Right X axis
        """
        self.update
        return(self.convert(self.gp.get_axes(button_map['RightX'])))

    def get_ry(self):
        """
        return value of Right Y axis
        """
        self.update
        return(self.convert(self.gp.get_button(button_map['RightY'])))

    def get_lx(self):
        """
        return value of Left X axis
        """
        self.update
        return(self.convert(self.gp.get_button(button_map['LeftX'])))

    def get_ly(self):
        """
        return value of Left Y axis
        """
        self.update
        return(self.convert(self.gp.get_button(button_map['LeftY'])))
