#!/usr/bin/env python
'''
tool to record a series of input commands for the serial switch conroller
'''
from pynput.keyboard import Listener, Key
from binascii import hexlify
from time import time_ns
from serial import Serial


def time_ms():
    return time_ns() // 1000000


STICK_MIN = 0x00
STICK_CENTER = 0x80
STICK_MAX = 0xff

# values to pass into button functions
Y = (1, 0x01)
B = (1, 0x02)
A = (1, 0x04)
X = (1, 0x08)
L = (1, 0x10)
R = (1, 0x20)
ZL = (1, 0x40)
ZR = (1, 0x80)
MINUS = (0, 0x01)
PLUS = (0, 0x02)
LCLICK = (0, 0x04)
RCLICK = (0, 0x08)
HOME = (0, 0x10)
CAPTURE = (0, 0x20)

# values to pass into stick functions
L_LEFT = (3, STICK_MIN)
L_RIGHT = (3, STICK_MAX)
L_UP = (4, STICK_MIN)
L_DOWN = (4, STICK_MAX)
R_LEFT = (5, STICK_MIN)
R_RIGHT = (5, STICK_MAX)
R_UP = (6, STICK_MIN)
R_DOWN = (6, STICK_MAX)


class CommandRecorder(object):
    def __init__(self, filename, device):
        self._filename = filename
        self._device = device
        self._state = bytearray([
            # Button H (MINUS, PLUS, LCLICK, RCLICK, HOME, CAPTURE)
            0x0,
            # Button L (Y, B, A, X, L, R, ZL, ZR)
            0x0,
            # HAT (not modified)
            0x8,
            # LX
            STICK_CENTER,
            # LY
            STICK_CENTER,
            # RX
            STICK_CENTER,
            # RY
            STICK_CENTER,
            # VendorSpec (not modified)
            0x0
        ])
        self._press_actions = {
            'p': lambda: self._button_set(A),
            'o': lambda: self._button_set(B),
            'i': lambda: self._button_set(X),
            'u': lambda: self._button_set(Y),
            'w': lambda: self._stick_set(L_UP),
            'a': lambda: self._stick_set(L_LEFT),
            's': lambda: self._stick_set(L_DOWN),
            'd': lambda: self._stick_set(L_RIGHT),
            'f': lambda: self._button_set(L),
            'g': lambda: self._button_set(ZL),
            'j': lambda: self._button_set(R),
            'h': lambda: self._button_set(ZR),
            'm': lambda: self._button_set(HOME),
            'c': lambda: self._button_set(CAPTURE),
            'v': lambda: self._button_set(MINUS),
            'n': lambda: self._button_set(PLUS),
            Key.up: lambda: self._stick_set(R_UP),
            Key.left: lambda: self._stick_set(R_LEFT),
            Key.down: lambda: self._stick_set(R_DOWN),
            Key.right: lambda: self._stick_set(R_RIGHT),
            Key.enter: lambda: self._file.write('\n')
        }
        self._release_actions = {
            'p': lambda: self._button_clr(A),
            'o': lambda: self._button_clr(B),
            'i': lambda: self._button_clr(X),
            'u': lambda: self._button_clr(Y),
            'w': lambda: self._stick_clr(L_UP),
            'a': lambda: self._stick_clr(L_LEFT),
            's': lambda: self._stick_clr(L_DOWN),
            'd': lambda: self._stick_clr(L_RIGHT),
            'f': lambda: self._button_clr(L),
            'g': lambda: self._button_clr(ZL),
            'j': lambda: self._button_clr(R),
            'h': lambda: self._button_clr(ZR),
            'm': lambda: self._button_clr(HOME),
            'c': lambda: self._button_clr(CAPTURE),
            'v': lambda: self._button_clr(MINUS),
            'n': lambda: self._button_clr(PLUS),
            Key.up: lambda: self._stick_clr(R_UP),
            Key.left: lambda: self._stick_clr(R_LEFT),
            Key.down: lambda: self._stick_clr(R_DOWN),
            Key.right: lambda: self._stick_clr(R_RIGHT),
            Key.enter: None
        }
        self._last_action = None

    def __enter__(self):
        self._file = open(self._filename, 'w')
        self._serial = Serial(self._device)
        self._kl = Listener(on_press=self._press, on_release=self._release)
        self._kl.setDaemon(True)
        self._ms = time_ms()
        self._kl.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._file.close()
        self._serial.close()
        self._kl.stop()

    def _button_set(self, button):
        self._state[button[0]] |= button[1]

    def _button_clr(self, button):
        self._state[button[0]] &= ~button[1]

    def _stick_set(self, stick):
        self._state[stick[0]] = stick[1]

    def _stick_clr(self, stick):
        self._state[stick[0]] = STICK_CENTER

    def _act(self, key, isPressed):
        try:
            keycode = key.char
        except AttributeError:
            keycode = key
        finally:
            action = self._press_actions.get(
                keycode, None) if isPressed else self._release_actions.get(keycode, None)

            if not action or action == self._last_action:
                return

            self._last_action = action

            # get current time
            ms = time_ms()

            # write old state with the duration it was active to file
            self._file.write('{} {}\n'.format(
                hexlify(self._state).decode(),
                ms - self._ms
            ))

            # update time
            self._ms = ms

            # perform action
            action()

            # send new state to serial
            # serial

    def _press(self, key):
        self._act(key, True)

    def _release(self, key):
        self._act(key, False)

    def record(self):
        # setup phase
        print('starting recording\n')
        input('recording setup. press enter to proceed\n')

        # loop phase
        input('recording loop. press enter to proceed\n')
        print('done recording\n')


def main(args):
    with CommandRecorder(args.filename, args.device) as cr:
        cr.record()


if __name__ == "__main__":
    from argparse import ArgumentParser
    import os.path

    # creating a parser
    parser = ArgumentParser(
        description='tool to record a series of input commands for the serial switch conroller'
    )

    # adding arguments
    parser.add_argument(
        "--file", "-f",
        dest="filename",
        required=True,
        help="where to store the commands",
        metavar="filename",
    )

    parser.add_argument(
        "--serial", "-s",
        dest="device",
        required=True,
        help="where to send the commands to",
        metavar="device_adress",
    )

    # parse arguments
    args = parser.parse_args()

    # run main program
    main(args)
