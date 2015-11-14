import HID
import sys

try:
    hid = HID.Gamepad()
except:
    hid = None
if hid is not None:
    jy = hid.get_ly()  # Left joystick Y axis
    jx = hid.get_rx()  # Right joystick X axis
else:
    jy = input("Enter a value for jy:")
    jx = input("Enter a value for jx:")

L1 = 0  # Left motor first set
R1 = 0  # Right motor first set

L2 = 0  # Left motor second set
R2 = 0  # Right motor second set


def main():
    while True:
        set1()  # calculate the first set of motors
        set2()  # calculate the second set of motors
        print("{}    {}\n{}    {}".format(L1, L2, R1, R2))
        # These values will probably have to change
        try:
            if hid.get_start() == 1:
                sys.exit()
        except:
            if input("Continue? (1/0)") == 1:
                global jy
                jy = input("Enter a value for jy:")
                global jx
                jx = input("Enter a value for jx:")
            else:
                sys.exit()


def set1():
    global L1
    L1 = (jy+jx)/2

    global R1
    L1 = (jy+(-1*jx))/2


def set2():
    global L2
    L2 = (jy+jx)/2  # ??


if __name__ == '__main__':
    main()
