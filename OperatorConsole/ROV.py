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
import time
import sys
from datetime import date

from Packet import Packet
import HID
import profiler
import error_handler

profile = profiler.profiler()
enable_profile = True  # set to True to enable profiling feaures
errors = error_handler.error_handler()  # used to store error messages

###############################################################################
# set up the gamepad
###############################################################################

hid_enable = True
hid = object
try:
    hid = HID.Gamepad(-100, 100)
except:
    error = ("ERROR: Failed to start gamepad interface, continuing anyways." +
             "Program operation will be severly limited." +
             "Check that all tether cables are securly connected and that " +
             "the gamepad is plugged in to the tether box.")
    errors.add(error)
    print error

    hid_enable = False
    time.sleep(1)  # give the user a chance to read message


def off():
    """
    Used for the button map dictionary
    """
    return 0


if hid_enable:
    bmap = {  # Button mapping. 'Function': corresponding method
        'X': hid.get_lx,  # X axis
        'Y': hid.get_ly,  # Y axis
        'Z': hid.get_ry,  # Z axis
        'Xr': None,  # X rotation axis
        'Yr': None,  # Y rotation axis
        'Zr': hid.get_rx,  # Z rotation axis
        'Light_up': hid.get_r1,  # increase brightness
        'Light_down': hid.get_l1,  # decrease brightness
        'Screen+': hid.get_start,  # cycle screens right
        'Screen-': None,  # cycle screens left
        'Select_left': hid.get_dpad_left,
        'Select_right': hid.get_dpad_right,
        'Select_up': hid.get_dpad_up,
        'Select_down': hid.get_dpad_down,
        'Enter': hid.get_x,
        'Increase': None,  # increase selected setting
        'Decrease': None,  # decrease selected setting
    }
else:  # set each function to off
    bmap = {  # Button mapping. Function: corresponding method
        'X': off,
        'Y': off,
        'Z': off,
        'Xr': off,
        'Yr': off,
        'Zr': off,
        'Light_up': off,  # increase brightness
        'Light_down': off,  # decrease brightness
        'Screen+': off,  # cycle screens right
        'Screen-': off,  # cycle screens left
        'Select_left': off,
        'Select_right': off,
        'Select_up': off,
        'Select_down': off,
        'Enter': off,
        'Increase': None,  # increase selected setting
        'Decrease': None,  # decrease selected setting
    }

# ser = serial.Serial('/dev/', 250000)

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
rotation = [0, 0, 0]  # rotational velocity around x, y, and z axis
acceleration = [0, 0, 0]

hlf = 0  # horizontal left front
hlb = 0  # horizontal left back
hrf = 0  # horizontal right front
hrb = 0  # horizontal right back
vlf = 0  # vertical left front
vlb = 0  # vertical left back
vrf = 0  # vertical right front
vrb = 0  # vertical right back

motor_pins = {'hlf':1,
              'hlb':motor_pins['hlf']+1,
              'hrf':motor_pins['hlf']+1,
              
}

brightness = 0  # Light brighteness. 0 = no light, 100 = full brightness
pan = 0
tilt = 0
depth = 0
heading = ""


def startup():
    """
    - load settings from file
    - establish communication with Propeller Chip
    """
    start_time = time.clock()

###############################################################################
# load settings from file
###############################################################################
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
###############################################################################

    # check for communication with rov
    try:
        # ser.setPort("")
        pass
    except:
        errors.add("ERROR: Can't connect to serial port.")
        print("ERROR: Can't connect to serial port.")
        time.sleep(1)

    end_time = time.clock()
    if enable_profile:
        profile.add({"Startup": end_time - start_time})


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


def velocity_toString():
    global velocity
    string = "X: %s " % velocity[0]
    string += "Y: %s " % velocity[1]
    string += "Z: %s " % velocity[2]
    return(string)


def acceleration_toString():
    global acceleration
    string = ("X: %s " % acceleration[0])
    string += "Y: %s " % acceleration[1]
    string += "Z: %s " % acceleration[2]
    return(string)


def calc_thrust(x, y, z):
    """
    Calculates the values for each motor in a vectored thrust configuration.
    """
    global hlf, hrf, hlb, hrb, vlf, vrf, vlb, vrb

    LFx = x
    RFx = -x
    LBx = x
    RBx = -x

    LFy = y
    RFy = y
    LBy = -y
    RBy = -y

    LFz = z
    RFz = -z
    LBz = -z
    RBz = z

    hlf = (LFx+LFy)/2
    hrf = -(RFx+RFy)/2
    hlb = -(LBx+LBy)/2
    hrb = (RBx+RBy)/2

    hlf = (hlf+LFz)/2
    hrf = (hrf+RFz)/2
    hlb = (hlb+LBz)/2
    hrb = (hrb+RBz)/2

    values = [abs(hlf), abs(hrf), abs(hlb), abs(hrb)]
    values.sort()

    # adjust so that thrust is maximised
    axis = [abs(x), abs(y), abs(z)]
    axis.sort()
    lim = axis[2]

    if (int(values[3]) is not 0):
        if hlf > 0:
            hlf = int(hlf+lim-values[3])
        else:
            hlf = int(hlf-(lim-values[3]))

        if hrf > 0:
            hrf = int(hrf+lim-values[3])
        else:
            hrf = int(hrf-(lim-values[3]))

        if hlb > 0:
            hlb = int(hlb+lim-values[3])
        else:
            hlb = int(hlb-(lim-values[3]))

        if hrb > 0:
            hrb = int(hrb+lim-values[3])
        else:
            hrb = int(hrb-(lim-values[3]))

    # vertical thrusters ######################################################
    vlf = bmap['Z']()
    vrf = bmap['Z']()
    vlb = bmap['Z']()
    vrb = bmap['Z']()

    if hid_enable:
        vlf += hid.get_r2() - hid.get_l2()
        if vlf > 100:
            vlf = 100

        if vlf < -100:
            vlf = -100
        vrf = vlf

        vlb += -hid.get_r2() + hid.get_l2()
        if vlb > 100:
            vlb = 100

        if vlb < -100:
            vlb = -100
        vrb = vlb


def update():
    """
    Should be called every cycle thru a mainloop. This gets input from the
    gamepad, sends new info to the microcontroller and recieves info from the
    microcontroller. Essentially this is the main function of the ROV program.
    """
    start_time = time.clock()
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
    global hlf, hlb, hrf, hrb, vlf, vlb, vrf, vrb

    y_axis = bmap['Y']()  # Left joystick Y axis
    x_axis = bmap['X']()  # Left joystick X axis
    zr_axis = bmap['Zr']()  # Right joystick X axis
    calc_thrust(y_axis, x_axis, zr_axis)

    end_time = time.clock()
    if enable_profile:
        profile.add({"update": end_time - start_time})


###############################################################################
# Screen methods
###############################################################################
def main_screen():
    """
    Displays important system stats such as heading, depth, and brightness
    """
    screen = ("Depth = {}ft\nHeading = {}\nVelocity(ft/s) = {}\n"
              "Acceleration() = {}"
              "\nBrighteness = {}".format(depth, heading,
                                          velocity_toString(),
                                          acceleration_toString(),
                                          brightness))
    return(screen)


def screen2():
    screen = "Screen 2"
    return(screen)


def error_screen():
    """
    Displays system errors
    """
    return(errors.toString())


def profile_screen():
    """
    displays info from the profiling system (execution time for different
    portions of the software)
    """
    return profile.toString()


def status_screen():
    """
    Shows the status of system variable not present on the main screen. Useful
    for debugging purposes.
    """
    global hlf, hlb, hrf, hrb, vlf, vlb, vrf, vrb
    screen = "System Status:\n"
    screen += "h:{} {}\n  {} {}\nv:{} {}\n  {} {}\n".format(hlf, hrf, hlb,
                                                            hrb, vlf, vrf,
                                                            vlb, vrb)
    return screen

###############################################################################
# Add the method for each screen to the "screens" list.
# This lets basic_gui know which screens are available.
# If more complex functionality is needed this may change to a dictionary, or
# nested list.
###############################################################################
screens = [main_screen, screen2, error_screen, profile_screen, status_screen]
screen_index = 0
current = 0
previous = 0


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
    start_time = time.clock()
    global current, previous
    current = bmap['Screen+']()

    # form1 = ("Depth = %sft | Heading = %s | Velocity(ft/s) = %d | "
    #          "Acceleration() = %d"
    #          "\nBrighteness = %\%s" % depth % heading % velocity_toString()
    #          % acceleration_toString() % brightness)

    # check if a cycle button is pressed
    # if so, increment or decrement screen index
    # run selected screen
    # check if output needs to be updated (old_out != new_out)
    global screen_index
    _buffer = ""  # store the output text from the active screen

    if bmap['Screen+']() == 1 and previous == 0:
        screen_index += 1
        if screen_index >= len(screens):
            screen_index = 0

    _buffer = screens[screen_index]()

    # Clear and print _buffer to screen
    sys.stderr.write("\x1b[2J\x1b[H")
    print(_buffer)

    previous = current

    end_time = time.clock()
    if enable_profile:
        profile.add({"gui": end_time - start_time})


def main():
    startup()
    while True:
        start_time = time.clock()
        update()
        basic_gui()

        end_time = time.clock()
        if enable_profile:
            profile.add({"main": end_time - start_time})


def __init__():
    pass


if __name__ == '__main__':
    main()
