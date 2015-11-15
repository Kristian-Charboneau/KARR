#! /usr/bin/env python
"""Main application for KARR. Provide's a basic "gui" using the terminal.
@author:Kristian Charboneau

This program can be used on its own or integrated into a GUI application.
When run standalone the main() method manages the program. It has a simple text
based gui when run standalone.

To integrate into an external GUI the startup() ans update() methods should be
called. Startup() should be called once, at the beginning of the program.
Update() should be called each cycle thru the GUI's mainloop.
"""
import serial
from Packet import Packet
import HID

hid_ = True
hid = object
try:
    hid = HID.Gamepad(-100, 100)
except:
    print("Failed to start gamepad interface, continuing anyways.")
    hid_ = False


ser = serial.Serial()

###############################################################################
# variables to store hardware and motion states
###############################################################################
velocity = [0, 0, 0]  # linear velocity on x, y, and z axis
rotation = [0, 0, 0]  # rotational speed around x, y, and z axis
light = 0  # Light brighteness. 0 = no light, 100 = full brightness
pan = 0
tilt = 0
depth = 0
heading = ""
brightness = 0


def startup():
    # do setup and initial stuff
    # check for communication with rov
    ser.setPort("")


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


def light(value):
    pass


def camera_pan(value):
    """
    Not used in the current version of KARR (kept for future use)
    """
    global pan
    pan = value


def camera_tilt(value):
    """
    Not used in the current version of KARR (kept for future use)
    """
    global tilt
    tilt = value


def velocity_toString():
    string = "X: %s " % velocity[0]
    string += "Y: %s " % velocity[1]
    string += "Z: %s " % velocity[2]
    return(string)


def acceleration_toString():
    string = "X: %s " % velocity[0]
    string += "Y: %s " % velocity[1]
    string += "Z: %s " % velocity[2]
    return(string)


def update():
    """
    Should be called every cycle thru a mainloop. This gets input from the
    gamepad, sends new info to the microcontroller and recieves info from the
    microcontroller. Essentially this is the main function of the ROV program.
    """
    # update gamepad controls (assign values to velocity and rotation)
    #
    # send information to microcontroller
    #   - Velocity and rotation get sent every cycle, other stuff gets sent
    #     whenever it changes
    #
    # receive info from microcontroller (add info to variables)
    #   - depth
    #
    # get info from IMU
    #   - velocity, acceleration, rotation, heading
    if hid_:
        pass  # update controls
    # update other stuff that doesn't depend on the gamepad


def basic_gui():
    """
    Creates a very basic "GUI" for displaying data and modifying things like
    the trim values. Uses the terminal for output. It basically just prints the
    same lines over and over again. To make the output look better the terminal
    should either be reistricted to the same size as the output or another
    window (perhaps a video feed viewer) should be used to cover the rest of
    the terminal. While this isn't fancy it should have less overhead than a
    full gui (I'm assuming) and it can be accessed over SSH, way may be useful
    at some point here or there.
    """

    # form1 = ("Depth = %sft | Heading = %s | Velocity(ft/s) = %d | "
    #          "Acceleration() = %d"
    #          "\nBrighteness = %\%s" % depth % heading % velocity_toString()
    #          % acceleration_toString() % brightness)
    form1 = ("Depth = {}ft | Heading = {} | Velocity(ft/s) = {} | "
             "Acceleration() = {}"
             "\nBrighteness = \{}".format(depth, heading, velocity_toString(),
                                          acceleration_toString(), brightness))
    print form1


def main():
    startup()
    update()
    basic_gui()
    # while True:
    print(hid.get_x())


def __init__():
    pass


if __name__ == '__main__':
    main()
