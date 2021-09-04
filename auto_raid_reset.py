from __future__ import annotations

import argparse
import calendar
import datetime
import sys
import time

import cv2
import numpy
import serial


SERIAL_DEFAULT = 'COM1' if sys.platform == 'win32' else '/dev/ttyUSB0'


TYPES = {  # (g, b, r) because dumb fucking cv2
    'ghost': (162, 104, 85),
    'flying': (203, 153, 135),
    'fire': (97, 147, 223),
    'normal': (152, 149, 141),
    'NONE': (88, 60, 213),
}


def _getframe(vid: cv2.VideoCapture) -> numpy.ndarray:
    _, frame = vid.read()
    cv2.imshow('game', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        raise SystemExit(0)
    return frame


def near_color(pixel: numpy.ndarray, expected: tuple[int, int, int]) -> bool:
    total = 0
    for c1, c2 in zip(pixel, expected):
        total += (c2 - c1) * (c2 - c1)

    return total < 76


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


def _wait_and_render(vid: cv2.VideoCapture, t: float) -> None:
    end = time.time() + t
    while time.time() < end:
        _getframe(vid)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', type=datetime.date.fromisoformat)
    parser.add_argument('--serial', default=SERIAL_DEFAULT)
    args = parser.parse_args()

    print('hello, welcome to the pogram')
    print('set up the controller thingy, and then enter the game')
    input('press enter when ready: ')

    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

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
            # INCREMENT CODE
            _press(ser, 'A')
            _wait_and_render(vid, 4)

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
            _wait_and_render(vid, .5)
            current_date = target_date
            print(f'date is now {current_date}')

            _return_to_game_from_date_panel(ser)

            _press(ser, 'B')
            _wait_and_render(vid, 1)
            _press(ser, 'A')
            _wait_and_render(vid, 5)
            _press(ser, 'A')
            _wait_and_render(vid, .5)
            _press(ser, 'A')
            _wait_and_render(vid, .5)
            _press(ser, 'A')

            frame = _getframe(vid)
            while not numpy.array_equal(frame[457][881], (16, 16, 16)):
                frame = _getframe(vid)

            # detect 5 star
            if not all(c >= 210 for c in frame[61][315]):
                continue

            print('found 5 star')

            # detect first type
            if not near_color(frame[115, 70], TYPES['normal']):
                continue

            print('found correct first type')

            # detect second type
            if not near_color(frame[115, 216], TYPES['NONE']):
                continue

            print('found correct second type')

            # channel points bets?
            input('pause for channel point betting... (press enter)')

            # SAVE AND CHECK
            _press(ser, 'B')
            _wait_and_render(vid, 2)
            _press(ser, 'X')
            _wait_and_render(vid, 1)
            _press(ser, 'R')
            _wait_and_render(vid, 2)
            _press(ser, 'A')
            _wait_and_render(vid, 5)

            _press(ser, 'A')
            _wait_and_render(vid, 1)
            _press(ser, 's')
            _press(ser, 'A')
            _wait_and_render(vid, .75)
            _press(ser, 'A')

            print('what would you like to do?')
            print('1: reset')
            print('q: quit')
            command = input('> ')
            if command == 'q':
                return 0
            elif command == '1':
                _press(ser, 'H')
                _wait_and_render(vid, 1)
                _press(ser, 'X')
                _wait_and_render(vid, 1)
                _press(ser, 'A')
                _wait_and_render(vid, 5)
                _press(ser, 'A')
                _wait_and_render(vid, 1)

                _press(ser, 'A')
                _wait_and_render(vid, 20)
                _press(ser, 'A')
                _wait_and_render(vid, 10)
                _press(ser, 'A')
                _wait_and_render(vid, 5)


if __name__ == '__main__':
    exit(main())
