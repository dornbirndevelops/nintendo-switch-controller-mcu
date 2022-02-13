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

    print('hello, welcome to the pogram')
    print('set up the controller thingy, and then enter the game')
    input('press enter when ready: ')

    with serial.Serial(args.serial, 9600) as ser:
        if args.date is not None:
            current_date = args.date
        else:
            _open_date_panel(ser)

            while True:
                date_s = input('what is the date YYYY-MM-DD? ')
                try:
                    current_date = datetime.date.fromisoformat(date_s)
                except ValueError:
                    continue
                else:
                    break

            _return_to_game_from_date_panel(ser)

        print(f'cool, the date is {current_date}')

        while True:
            print('what would you like to do?')
            print('1: increment date')
            print('2: save and check')
            print('3: reset')
            print('q: quit')
            command = input('> ')
            if command == 'q':
                return 0
            elif command == '1':
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
            elif command == '2':
                _press(ser, 'B')
                time.sleep(2)
                _press(ser, 'X')
                time.sleep(1)
                _press(ser, 'R')
                time.sleep(2)
                _press(ser, 'A')
                time.sleep(5)

                _press(ser, 'A')
                time.sleep(1)
                _press(ser, 's')
                _press(ser, 'A')
                time.sleep(.75)
                _press(ser, 'A')
            elif command == '3':
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
                _press(ser, 'A')


if __name__ == '__main__':
    raise SystemExit(main())
