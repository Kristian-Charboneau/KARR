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
import pickle
from Packet import Packet
import HID

hid_ = True
hid = object
try:
    hid = HID.Gamepad(-100, 100)
except:
    print("Failed to start gamepad interface, continuing anyways.")
    hid_ = False

ser = serial.Serial('/dev/', 250000)

save_file = "settings.obj"
save_data = []
# save_data structure: [LF_trim, RF_trim, LB_trim, RB_trim, LFV_trim, RFV_trim,
# LBV_trim, RBV_trim, brightness]

###############################################################################
# variables to store settings
###############################################################################
LF_trim = 0
RF_trim = 0
LB_trim = 0
RB_trim = 0
LFV_trim = 0
RFV_trim = 0
LBV_trim = 0
RBV_trim = 0

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
    """
    - load settings from file
    - establish communication with Propeller Chip
    """

    # load settings from file
    global save_data
    global LF_trim, RF_trim, LB_trim, RB_trim, LFV_trim, RFV_trim, LBV_trim
    global RBV_trim, brightness

    try:
        fileObject = open(save_file, 'r')
    except:  # use default values if no save file found
        pass
    else:  # load values from savefile
        save_data = pickle.load(fileObject)
        LF_trim = save_data[0]
        RF_trim = save_data[1]
        LB_trim = save_data[2]
        RB_trim = save_data[3]
        LFV_trim = save_data[4]
        RFV_trim = save_data[5]
        LBV_trim = save_data[6]
        RBV_trim = save_data[7]
        brightness = save_data[8]

    # check for communication with rov
    ser.setPort("")


def shutdown():
    """
    Shutdown procedures:
    - save settings to file
    - tell Propeller Chip to start shutdown sequence
    - Tell system to shutdown
    """
    fileObject = open(save_file, 'wb')
    pickle.dump(save_data, fileObject)

    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output


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
