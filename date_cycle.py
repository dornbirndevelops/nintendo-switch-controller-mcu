from __future__ import annotations

import argparse
import calendar
import datetime
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


def _open_date_panel(ser: serial.Serial) -> None:
    _press(ser, 'H')
    time.sleep(.8)

    _press(ser, 's')
    _press(ser, 'd', duration=.55)
    _press(ser, 'A')
    time.sleep(1)

    _press(ser, 's', duration=1.2)
    _press(ser, 'A')
    time.sleep(.75)

    _press(ser, 's', duration=.5)
    _press(ser, 'A')
    time.sleep(.75)

    for i in range(2):
        _press(ser, 's')
    _press(ser, 'A')
    time.sleep(.75)


def _return_to_game_from_date_panel(ser: serial.Serial) -> None:
    _press(ser, 'H')
    time.sleep(1)
    _press(ser, 'H')
    time.sleep(2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', type=datetime.date.fromisoformat)
    parser.add_argument('--serial', default=SERIAL_DEFAULT)
    args = parser.parse_args()

    current_date = args.date

    with serial.Serial(args.serial, 9600) as ser:
        while True:
            _press(ser, 'A')
            time.sleep(4)

            _open_date_panel(ser)

            target_date = current_date + datetime.timedelta(days=1)
            if current_date.month != target_date.month:
                _press(ser, 'w')
            _press(ser, 'd')
            _press(ser, 'w')
            if current_date.month != target_date.month:
                _, target_max_days = calendar.monthrange(
                    target_date.year,
                    target_date.month,
                )
                for _ in range(target_max_days - current_date.day):
                    _press(ser, 'w')
            _press(ser, 'd')
            if current_date.year != target_date.year:
                _press(ser, 'w')
            _press(ser, 'd', duration=.5)
            _press(ser, 'A')
            time.sleep(.5)
            current_date = target_date
            print(f'date is now {current_date}')

            _return_to_game_from_date_panel(ser)

            _press(ser, 'B')
            time.sleep(1)
            _press(ser, 'A')
            time.sleep(5)
            _press(ser, 'A')
            time.sleep(.5)
            _press(ser, 'A')
            time.sleep(.5)
            _press(ser, 'A')
            time.sleep(2)


if __name__ == '__main__':
    exit(main())
