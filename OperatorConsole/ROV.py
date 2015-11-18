#! /usr/bin/env python
"""Main application for KARR. Provide's a basic "gui" using the terminal.
@author:Kristian Charboneau

This program can be used on its own or integrated into a GUI application.
When run standalone the main() method manages the program. It has a simple text
based gui when run standalone.

To integrate into an external GUI the startup() and update() methods should be
called. Startup() should be called once, at the beginning of the program.
Update() should be called each cycle thru the GUI's mainloop.
"""
import serial
import pickle
from Packet import Packet
import HID
import time

profile = True  # set to True to enable profiling feaures
errors = ""  # used to store error messages

###############################################################################
# set up the gamepad
###############################################################################

hid_ = True
hid = object
try:
    hid = HID.Gamepad(-100, 100)
except:
    error = ("ERROR: Failed to start gamepad interface, continuing anyways." +
             "Program operation will be severly limited." +
             "Check that all tether cables are securly connected and that " +
             "the gamepad is plugged in to the tether box.")
    errors += error
    print error

    hid_connected = False

bmap = {  # Button mapping. Function: corresponding method
    'X': hid.get_lx,
    'Y': hid.get_ly,
    'Z': None,
    'Xr': hid.get_ry,
    'Yr': None,
    'Zr': hid.get_rx,
    'Light_up': hid.get_r1,  # increase brightness
    'Light_down': hid.get_l1,  # decrease brightness
    'Screen+': hid.get_start,  # cycle screens right
    'Screen-': None,  # cycle screens left
    'Select_left': hid.get_dpad_left,
    'Select_right': hid.get_dpad_right,
    'Select_up': hid.get_dpad_up,
    'Select_down': hid.get_dpad_down,
    'Enter': hid.get_x

}
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
    start_time = time.time()

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

    end_time = time.time()
    if profile:
        exec_time = end_time - start_time


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
    start_time = time.time()
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

    end_time = time.time()
    if profile:
        exec_time = end_time - start_time


###############################################################################
# Screen methods
###############################################################################
def screen1():
    screen = ("Depth = {}ft | Heading = {} | Velocity(ft/s) = {} | "
              "Acceleration() = {}"
              "\nBrighteness = \{}".format(depth, heading,
                                           velocity_toString(),
                                           acceleration_toString(),
                                           brightness))
    return(screen)


def screen2():
    screen = "Screen 2"
    return(screen)

###############################################################################
# Add the method for each screen to the "screens" list.
# This lets basic_gui know which screens are available.
# If more complex functionality is needed this may change to a dictionary, or
# nested list.
###############################################################################
screens = [screen1]


def basic_gui():
    """
    Creates a very basic "GUI" for displaying data and modifying things like
    the trim values. Uses the terminal for output. It basically just prints the
    same lines over and over again, with a "clear" command used to clean things
    up (so there aren't thousands of lines on the terminal). The output is
    split up into "screens". One screen is displayed at a time.

    Each screen should be a method that generates and returns a string. That
    string is then printed to the screen by basic_gui(). The screen methods are
    stored in a list called "screens". Basic_gui will use this list when the
    user cycles through screens.

    While this isn't fancy it should have less overhead than a full gui
    (I'm assuming) and it can be accessed over SSH, which may be useful at some
    point here or there.
    """
    start_time = time.time()

    # form1 = ("Depth = %sft | Heading = %s | Velocity(ft/s) = %d | "
    #          "Acceleration() = %d"
    #          "\nBrighteness = %\%s" % depth % heading % velocity_toString()
    #          % acceleration_toString() % brightness)

    # check if a cycle button is pressed
    # if so, increment or decrement screen index
    # run selected screen
    # check if output needs to be updated (old_out != new_out)

    if bmap['Screen+']() == 1:
        print(screens)

    print(screen1())

    end_time = time.time()
    if profile:
        exec_time = end_time - start_time


def main():
    start_time = time.time()
    startup()
    update()
    basic_gui()
    # while True:
    print(hid.get_x())

    end_time = time.time()
    if profile:
        exec_time = end_time - start_time


def __init__():
    pass


if __name__ == '__main__':
    main()
