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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--serial', default=SERIAL_DEFAULT)
    args = parser.parse_args()

    with serial.Serial(args.serial, 9600) as ser:
        _press(ser, 'H')
        time.sleep(1)
        _press(ser, 'X')
        time.sleep(1)
        _press(ser, 'A')
        time.sleep(5)
        _press(ser, 'A')
        time.sleep(1)

        _press(ser, 'A')
        time.sleep(20)
        _press(ser, 'A')
        time.sleep(10)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
