from __future__ import annotations

import argparse
import sys
import time

import serial

SERIAL_DEFAULT = 'COM1' if sys.platform == 'win32' else '/dev/ttyUSB0'


def _press(ser: serial.Serial, s: str, duration: float = .05) -> None:
    print(f'{s=} {duration=}')
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
    parser.add_argument('--part1', choices=('top', 'bottom'), required=True)
    parser.add_argument('--part2', choices=('top', 'bottom'), required=True)
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--serial', default=SERIAL_DEFAULT)
    args = parser.parse_args()

    assert args.part1 == 'top', f'{args.part1} not yet implemented'
    assert args.part2 == 'top', f'{args.part2} not yet implemented'

    with serial.Serial(args.serial, 9600) as ser:
        for i in range(args.count):
            print(f'reviving fossil #{i + 1}')
            _press(ser, 'A')
            time.sleep(1)
            _press(ser, 'A')
            time.sleep(1.1)
            _press(ser, 'A')
            time.sleep(1.1)
            _press(ser, 'A')
            time.sleep(1.1)
            _press(ser, 'A')
            time.sleep(.9)
            _press(ser, 'A')
            time.sleep(3.8)
            _press(ser, 'A')
            time.sleep(.9)
            _press(ser, 'A')
            time.sleep(.8)
            _press(ser, 'A')
            time.sleep(.6)
            _press(ser, 'A')
            time.sleep(4.2)
            _press(ser, 'A')
            time.sleep(1.5)
            _press(ser, 'A')
            time.sleep(1.5)

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
    exit(main())
