from __future__ import annotations

import os.path
import sys

import serial


def main():
    with serial.Serial(sys.argv[1], 9600) as ser:
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


if __name__ == '__main__':
    exit(main())
