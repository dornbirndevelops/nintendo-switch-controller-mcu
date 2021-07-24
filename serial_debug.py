from __future__ import annotations

import argparse
import os.path
import sys

import serial

SERIAL_DEFAULT = 'COM1' if sys.platform == 'win32' else '/dev/ttyUSB0'


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--serial', default=SERIAL_DEFAULT)
    args = parser.parse_args()

    with serial.Serial(args.serial, 9600) as ser:
        ser.write(b'V')
        while True:
            if os.path.exists('f'):
                with open('f', 'rb') as f:
                    contents = f.read()
                os.remove('f')
                ser.write(contents)
                sys.stdout.buffer.write(b'> send: ')
                sys.stdout.buffer.write(contents)
                sys.stdout.buffer.write(b'\n')
                sys.stdout.buffer.flush()
            elif ser.in_waiting:
                sys.stdout.buffer.write(ser.read())
                sys.stdout.buffer.flush()
    return 0


if __name__ == '__main__':
    exit(main())
