###############################################################################
# Operator console program for KARR
# Kristian Charboneau
##
###############################################################################

# -----------------------------------------------------------------------------
# This is a prototype application for controlling KARR. It uses a USB gamepad
# as input. It only displays status information and controls, no video feed for
# now. Instead another program (perhaps VLC) is used the display video from the
# ROV.
# -----------------------------------------------------------------------------

from Tkinter import *
# import pygame
import serial
import ROV as rov


class App:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.button = Button(
            frame, text="QUIT", fg="red", command=frame.quit)

        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

    def say_hi(self):
        print "hi there, everyone!"

    def update():
        rov.update()
        root.after(0, self.update)


root = Tk()

app = App(root)


root.mainloop()
root.destroy()


def get_movx():
    pass


def get_movy():
    pass


def get_movz():
    pass


def get_rotx():
    pass


def get_roty():
    pass


def get_rotz():
    pass
