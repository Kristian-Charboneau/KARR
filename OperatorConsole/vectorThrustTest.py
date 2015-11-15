"""
vectorThrustTest.py
Kristian Charboneau

A script for experimenting with different vector thrust algorithms.

Output looks like this:

LF  RF
LB  RB

With LF, RF, LB, and RB replaced with their thrust values.
Each motor has a range of -100 to 100. (-100 being reverse, 0 off, 100 forward)
"""
import HID
import sys

try:
    hid = HID.Gamepad()
except:
    hid = None
    print("No gamepad found.\n")

LF = 0  # Left front motor
RF = 0  # Right front motor

LB = 0  # Left back motor
RB = 0  # Right back motor


def main():
    while True:
        if hid is None:  # use keyboard input
            if input("Continue? (1/0)") == 1:
                # global y_axis
                y_axis = input("Enter a value for y axis:")
                # global x_axis
                x_axis = input("Enter a value for x axis:")
                # global z_axis
                z_axis = input("Enter a value for z axis:")
            else:
                sys.exit()
        else:  # use gamepad
            if hid.get_start() == 1:
                    sys.exit()

            # print(hid.get_ly(), hid.get_lx(), hid.get_rx())
            # print(hid.get_x(), hid.get_start())
            # global x_axis, y_axis, z_axis
            y_axis = hid.get_ly()  # Left joystick Y axis
            # print(y_axis)
            x_axis = hid.get_lx()  # Left joystick X axis
            # print(x_axis)
            z_axis = hid.get_rx()  # Right joystick X axis
            # print(z_axis)
        sys.stderr.write("\x1b[2J\x1b[H")

        calc(y_axis, x_axis, z_axis)
        global LF, RF, LB, RB

        # sys.stderr.write("\x1b[2J\x1b[H")  # clear the screen
        print("X:{} Y:{} Z:{}".format(x_axis, y_axis, z_axis))
        print("{}    {}\n{}    {}".format(LF, RF, LB, RB))


def checkEqual(lst):
    return not lst or lst.count(lst[0]) == len(lst)


def calc(x, y, z):  # x, y, and z axis
    global LF, RF, LB, RB

    # Initial mixing
    LF = (x + y + z)/3.0
    RF = (-1*x + y - z)/3.0
    LB = (x - y - z)/3.0
    RB = (-1*x - y + z)/3.0

    values = [abs(LF), abs(RF), abs(LB), abs(RB)]
    print(values)
    values.sort()
    print(values)

    # adjust so that thrust is maximised
    if (int(values[3]) is not 0) and not checkEqual(values):
        # print(values[3])
        print("adjusting!")
        LF = int(LF * (100/values[3]))
        RF = int(RF * (100/values[3]))
        LB = int(LB * (100/values[3]))
        RB = int(RB * (100/values[3]))
    else:
        LF = int(LF * 3)
        RF = int(RF * 3)
        LB = int(LB * 3)
        RB = int(RB * 3)

if __name__ == '__main__':
    main()
