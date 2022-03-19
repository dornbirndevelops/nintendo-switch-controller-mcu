from __future__ import annotations

import argparse
import sys
import time

import serial

SERIAL_DEFAULT = 'COM1' if sys.platform == 'win32' else '/dev/ttyUSB0'


def _press(ser: serial.Serial, s: str, duration: float = .05) -> None:
    ser.write(s.encode())
    time.sleep(duration)
    ser.write(b'0')
    time.sleep(.075)


def _beep(ser: serial.Serial) -> None:
    ser.write(b'!')
    time.sleep(.25)
    ser.write(b'.')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--serial', default=SERIAL_DEFAULT)
    args = parser.parse_args()

    with serial.Serial(args.serial, 9600) as ser:
        for i in range(args.count):
            print(f'reviving ~#{i + 1}')

            end = time.time() + 17.4
            while time.time() < end:
                _press(ser, 'A')

        print('backing out')
        end = time.time() + 5
        while time.time() < end:
            _press(ser, 'B')

        _press(ser, 'X')
        time.sleep(.5)
        _press(ser, 'A')
        time.sleep(2.4)
        _press(ser, 'A')
        time.sleep(.75)
        _press(ser, 'A')
        time.sleep(1)
        _press(ser, 'd')

        _beep(ser)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
