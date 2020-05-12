#!/usr/bin/env python
'''
tool to record a series of input commands for the serial switch conroller
/dev/ttyS0



  setup phase
  run once

  loop phase
  repeated many (n) times

  record:
  r - start setup recording
  now record every input with its timing for the setup
  r - stop setup recording and start loop recording
  now record every input with its timing for the loop
  r - stop loop recording
  now the file with the setup inputs and the loop inputs is stored

'''
from time import time_ns
from serial import Serial
from binascii import hexlify


def time_ms():
    return time_ns() // 1000000


class CommandRecorder(object):
    def __init__(self, filename, device):
        self._filename = filename
        self._device = device

    def __enter__(self):
        self._file = open(self._filename, 'w')
        self._serial = Serial(self._device)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._file.close()
        self._serial.close()

    def start(self):
        # initialize state only in the beginning
        if not self._state:
            self._state = bytearray(
                [
                    # Button H
                    0x0,
                    # Button L
                    0x0,
                    # HAT
                    0x8,
                    # LX
                    0x80,
                    # LY
                    0x80,
                    # RX
                    0x80,
                    # RY
                    0x80,
                    # VendorSpec
                    0x0
                ]
            )
        self._ms = time_ms()

    def stop(self):
        self._persist()

        # add empty line
        self._file.write('\n')

    def _persist(self):
        # get current time
        ms = time_ms()

        # write "state timediff" to file
        self._file.write('{} {}\n'.format(
            hexlify(self._state).decode(),
            ms - self._ms
        ))

        # update time
        self._ms = ms

    def _communicate(self):
        # send command
        self._serial.write(self._state)

    def button_set(self, button):
        # persist
        self._persist()

        # perform update
        self._state[button[0]] |= button[1]

        # communicate
        self._communicate()

    def button_clr(self, button):
        # persist
        self._persist()

        # perform update
        self._state[button[0]] &= ~button[1]

        # communicate
        self._communicate()

    def stick_set(self, stick):
        # persist
        self._persist()

        # perform update
        self._state[stick[0]] = stick[1]

        # communicate
        self._communicate()

    def stick_clr(self, stick):
        # persist
        self._persist()

        # perform update
        self._state[stick[0]] = 0x80

        # communicate
        self._communicate()


def main(args):
    '''
    create a recording of a series of input commands and store them in a file
    '''
    HAT_TOP = 0x00
    HAT_TOP_RIGHT = 0x01
    HAT_RIGHT = 0x02
    HAT_BOTTOM_RIGHT = 0x03
    HAT_BOTTOM = 0x04
    HAT_BOTTOM_LEFT = 0x05
    HAT_LEFT = 0x06
    HAT_TOP_LEFT = 0x07
    HAT_CENTER = 0x08

    STICK_MIN = 0x00
    STICK_CENTER = 0x80
    STICK_MAX = 0xff

    # values to pass into button functions
    SWITCH_Y = (1, 0x01)
    SWITCH_B = (1, 0x02)
    SWITCH_A = (1, 0x04)
    SWITCH_X = (1, 0x08)
    SWITCH_L = (1, 0x10)
    SWITCH_R = (1, 0x20)
    SWITCH_ZL = (1, 0x40)
    SWITCH_ZR = (1, 0x80)
    SWITCH_MINUS = (0, 0x01)
    SWITCH_PLUS = (0, 0x02)
    SWITCH_LCLICK = (0, 0x04)
    SWITCH_RCLICK = (0, 0x08)
    SWITCH_HOME = (0, 0x10)
    SWITCH_CAPTURE = (0, 0x20)

    # values to pass into stick functions
    L_LEFT = (3, STICK_MIN)
    L_RIGHT = (3, STICK_MAX)
    L_UP = (4, STICK_MIN)
    L_DOWN = (4, STICK_MAX)
    R_LEFT = (5, STICK_MIN)
    R_RIGHT = (5, STICK_MAX)
    R_UP = (6, STICK_MIN)
    R_DOWN = (6, STICK_MAX)

    with CommandRecorder(args.filename, args.device) as cr:
        print('press enter to start setup recording')
        # press enter
        cr.start()
        # state is initialized
        # ms is initialized

        import curses
        curses.KEY_F46
        # press "a" which is a button
        cr.button_set(SWITCH_A)

        # release "a" which is a button
        cr.button_clr(SWITCH_A)

        print('press enter to stop setup recording')
        # press enter a second time
        cr.stop()

        print('press enter to start loop recording')
        # press enter a third time
        cr.start()

        # press "a" which is a button
        cr.button_set(SWITCH_A)

        # release "a" which is a button
        cr.button_clr(SWITCH_A)

        print('press enter to stop loop recording')
        cr.stop()

    print('finished')


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


#     # represent & initialize state
#     ButtonH = 0
#     ButtonL = 0
#     HAT = 8
#     LX = STICK_CENTER
#     LY = STICK_CENTER
#     RX = STICK_CENTER
#     RY = STICK_CENTER
#     VendorSpec = 0
#     state = bytearray([ButtonH, ButtonL, HAT, LX, LY, RX, RY, VendorSpec])

#     # manipulate state
#     # buttons change a bit
#     def button_set(button):
#         state[button[0]] |= button[1]

#     def button_clr(button):
#         state[button[0]] &= ~button[1]

#     # sticks change a byte
#     def stick_set(stick):
#         state[stick[0]] = stick[1]

#     def stick_clr(stick):
#         state[stick[0]] = STICK_CENTER

#     # some key is pressed. each key knows its bit or byte it manipulates
#     import serial
#     ser = serial.Serial('/dev/ttyS0')
#     ser.write(state)

#     # close it in the end
#     ser.close()
