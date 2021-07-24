from __future__ import annotations

import argparse
import sys
import time

import serial

SERIAL_DEFAULT = 'COM1' if sys.platform == 'win32' else '/dev/ttyUSB0'


def _press(ser: serial.Serial, s: str, *, duration: float = .05) -> None:
    ser.write(s.encode())
    time.sleep(duration)
    ser.write(b'0')
    time.sleep(.15)


def _release(ser: serial.Serial, box_offset: int, box_n: int) -> None:
    _press(ser, 'A')
    time.sleep(1.75)
    _press(ser, 'A')
    time.sleep(1)
    _press(ser, 'A')
    time.sleep(8)

    # move to game boxes
    for _ in range(6):
        _press(ser, 'd')
        time.sleep(.1)

    # move offset to correct position
    for _ in range(box_offset):
        _press(ser, 'R')
        time.sleep(1.25)

    for _ in range(box_n):
        # box 1
        _press(ser, 'A')
        time.sleep(1)
        _press(ser, 'w')
        _press(ser, 'w')
        _press(ser, 'A')
        time.sleep(1.25)
        _press(ser, 's')
        _press(ser, 'A')
        time.sleep(.5)

        # mark first 4 rows
        for _ in range(2):
            for _ in range(5):
                _press(ser, 'd')
                _press(ser, 'A')
            _press(ser, 's')
            _press(ser, 'A')
            for _ in range(5):
                _press(ser, 'a')
                _press(ser, 'A')
            _press(ser, 's')
            _press(ser, 'A')

        # mark last row
        for _ in range(5):
            _press(ser, 'd')
            _press(ser, 'A')

        # return to 0, 0
        for _ in range(4):
            _press(ser, 'w')
        for _ in range(5):
            _press(ser, 'a')

        # perform the release
        _press(ser, '+')
        time.sleep(1.5)
        _press(ser, 'w')
        _press(ser, 'A')
        time.sleep(2)
        _press(ser, 'A')
        time.sleep(2.5)

        # on to the next box!
        _press(ser, 'R')
        time.sleep(1.25)

    # save back to title
    _press(ser, '+')
    time.sleep(2)
    _press(ser, 'A')
    time.sleep(15)
    _press(ser, 'A')
    time.sleep(3)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('box_count', type=int)
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--serial', default=SERIAL_DEFAULT)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    todo = args.box_count - args.offset
    offset = args.offset

    with serial.Serial(args.serial, 9600) as ser:
        while todo:
            if todo >= 3:
                box_n = 3
            else:
                box_n = todo

            if args.dry_run:
                for i in range(offset, offset + box_n):
                    print(f'would release box {i + 1}')
            else:
                _release(ser, offset, box_n)
            todo -= box_n
            offset += box_n

    return 0


if __name__ == '__main__':
    exit(main())
