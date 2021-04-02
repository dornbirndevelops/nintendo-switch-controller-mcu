from __future__ import annotations

import argparse
import time

import serial


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
    parser.add_argument(
        '--fossil',
        choices=('dracozolt', 'arctofish', 'arctozolt', 'dracovish'),
        required=True,
    )
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--serial', default='/dev/ttyUSB0')
    args = parser.parse_args()

    assert args.fossil == 'dracozolt', f'{args.fossil} not yet implemented'

    with serial.Serial(args.serial, 9600) as ser:
        for _ in range(args.count):
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
