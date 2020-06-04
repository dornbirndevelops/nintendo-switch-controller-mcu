#!/usr/bin/env python
'''
create a bot script by play through
'''
from argparse import ArgumentParser
from binascii import hexlify
from math import ceil
from serial import Serial
from signal import pause
from time import sleep, time_ns
from xbox360controller import Xbox360Controller

# helper variables
STICK_MIN = 0x00
STICK_CENTER = 0x80
STICK_MAX = 0xff

DPAD_TOP = 0x00
DPAD_TOP_RIGHT = 0x01
DPAD_RIGHT = 0x02
DPAD_BOTTOM_RIGHT = 0x03
DPAD_BOTTOM = 0x04
DPAD_BOTTOM_LEFT = 0x05
DPAD_LEFT = 0x06
DPAD_TOP_LEFT = 0x07
DPAD_CENTER = 0x08

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

L_STICK = (3, 4)
R_STICK = (5, 6)

dpad_positions = (
    (
        DPAD_BOTTOM_LEFT,
        DPAD_LEFT,
        DPAD_TOP_LEFT,
    ),
    (
        DPAD_BOTTOM,
        DPAD_CENTER,
        DPAD_TOP,
    ),
    (
        DPAD_BOTTOM_RIGHT,
        DPAD_RIGHT,
        DPAD_TOP_RIGHT,
    ),
)


# helper functions
_a = -1
_b = 1
_a2 = STICK_MIN
_b2 = STICK_MAX


def transform(v):
    return ceil(((v - _a) / (_b - _a)) * (_b2 - _a2) + _a2)


def time_ms():
    return time_ns() // 1000000


class BotRecorder(object):
    def __init__(self, filename, device):
        self._filename = filename
        self._device = device
        self._state = bytearray([
            # Button H (MINUS, PLUS, LCLICK, RCLICK, HOME, CAPTURE)
            0x0,
            # Button L (Y, B, A, X, L, R, ZL, ZR)
            0x0,
            # DPAD
            DPAD_CENTER,
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

    def __enter__(self):
        self._file = open(self._filename, 'w')
        self._serial = Serial(self._device)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._file.close()
        self._serial.close()

    def _before_event(self):
        # get current time
        ms = time_ms()

        # write old state with the duration it was active to file
        self._file.write('{} {}\n'.format(
            hexlify(self._state).decode(),
            ms - self._ms
        ))

        # update time
        self._ms = ms

    def _after_event(self):
        self._serial.write(self._state)

    def button_press(self, button):  # works
        self._before_event()
        self._state[button[0]] |= button[1]
        self._after_event()

    def button_release(self, button):  # works
        self._before_event()
        self._state[button[0]] &= ~button[1]
        self._after_event()

    def trigger_move(self, rawaxis, trigger):  # works but inaccurate
        if rawaxis.value > 0.5:
            self.button_press(trigger)
        else:
            self.button_release(trigger)

    def dpad_move(self, axis):  # works but with side-effect
        # neutral position is not recognized by driver
        # therefore send the neutral command after sending the registered command
        self._before_event()
        self._state[2] = dpad_positions[axis.x + 1][axis.y + 1]
        self._after_event()

        sleep(1 / 60)

        self._before_event()
        self._state[2] = DPAD_CENTER
        self._after_event()

    def stick_move(self, axis, stick):  # works but inaccurate
        self._before_event()
        self._state[stick[0]] = transform(round(axis.x))
        self._state[stick[1]] = transform(round(axis.y))
        self._after_event()

    def start(self):
        self._ms = time_ms()

    def next_phase(self):
        self._before_event()
        self._file.write('\n')


def main(args):
    with BotRecorder(args.filename, args.device) as recorder, Xbox360Controller(0) as controller:
        input('hit enter to start recording\n')

        # Axis
        # Sticks
        controller.axis_l.when_moved = lambda a: recorder.stick_move(
            a, L_STICK)
        controller.axis_r.when_moved = lambda a: recorder.stick_move(
            a, R_STICK)

        # DPAD
        controller.hat.when_moved = lambda a: recorder.dpad_move(a)

        # Raw Axis
        # Trigger
        controller.trigger_l.when_moved = lambda ra: recorder.trigger_move(
            ra, ZL)
        controller.trigger_r.when_moved = lambda ra: recorder.trigger_move(
            ra, ZR)

        # Buttons
        # are mapped to the switch button layout
        controller.button_b.when_pressed = lambda b: recorder.button_press(A)
        controller.button_b.when_released = lambda b: recorder.button_release(
            A)
        controller.button_a.when_pressed = lambda b: recorder.button_press(B)
        controller.button_a.when_released = lambda b: recorder.button_release(
            B)
        controller.button_y.when_pressed = lambda b: recorder.button_press(X)
        controller.button_y.when_released = lambda b: recorder.button_release(
            X)
        controller.button_x.when_pressed = lambda b: recorder.button_press(Y)
        controller.button_x.when_released = lambda b: recorder.button_release(
            Y)
        controller.button_trigger_l.when_pressed = lambda b: recorder.button_press(
            L)
        controller.button_trigger_l.when_released = lambda b: recorder.button_release(
            L)
        controller.button_trigger_r.when_pressed = lambda b: recorder.button_press(
            R)
        controller.button_trigger_r.when_released = lambda b: recorder.button_release(
            R)
        controller.button_mode.when_pressed = lambda b: recorder.button_press(
            HOME)
        controller.button_mode.when_released = lambda b: recorder.button_release(
            HOME)
        controller.button_select.when_pressed = lambda b: recorder.button_press(
            MINUS)
        controller.button_select.when_released = lambda b: recorder.button_release(
            MINUS)
        controller.button_start.when_pressed = lambda b: recorder.button_press(
            PLUS)
        controller.button_start.when_released = lambda b: recorder.button_release(
            PLUS)
        controller.button_thumb_l.when_pressed = lambda b: recorder.button_press(
            LCLICK)
        controller.button_thumb_l.when_released = lambda b: recorder.button_release(
            LCLICK)
        controller.button_thumb_r.when_pressed = lambda b: recorder.button_press(
            RCLICK)
        controller.button_thumb_r.when_released = lambda b: recorder.button_release(
            RCLICK)

        recorder.start()

        print('setup recording started...\n')
        input('hit enter to proceed to loop phase\n')

        recorder.next_phase()

        print('loop recording started...\n')
        input('hit enter to finish\n')
        print('done')


if __name__ == "__main__":
    # creating a parser
    parser = ArgumentParser(
        description='create a bot script by play through'
    )

    # adding arguments
    parser.add_argument(
        "--file", "-f",
        dest="filename",
        required=True,
        help="where to store the bot commands",
        metavar="filename",
    )

    parser.add_argument(
        "--serial", "-s",
        dest="device",
        required=True,
        help="where to send the bot commands to",
        metavar="device_adress",
    )

    # parse arguments
    args = parser.parse_args()

    # run main program
    main(args)
