from __future__ import annotations

import argparse
import contextlib
import sys
import time
from typing import Generator

import cv2
import numpy
import serial

SERIAL_DEFAULT = 'COM1' if sys.platform == 'win32' else '/dev/ttyUSB0'


def _press(ser: serial.Serial, s: str, duration: float = .1) -> None:
    print(f'{s=} {duration=}')
    ser.write(s.encode())
    time.sleep(duration)
    ser.write(b'0')
    time.sleep(.075)


def _getframe(vid: cv2.VideoCapture, *, guide: bool = True) -> numpy.ndarray:
    _, frame = vid.read()

    if guide:
        px_1 = int(len(frame[0]) * 480 / 1510)
        px_2 = int(len(frame[0]) * 520 / 1510)
        py = int(len(frame) * 135 / 850)
        for px in (px_1, px_2):
            cv2.rectangle(
                frame,
                (px - 2, py - 2),
                (px + 2, py + 2),
                (0, 0, 255),
                2,
            )

    cv2.imshow('game', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        raise SystemExit(0)
    return frame


def _wait_and_render(vid: cv2.VideoCapture, t: float) -> None:
    end = time.time() + t
    while time.time() < end:
        _getframe(vid)


def _alarm(ser: serial.Serial, vid: cv2.VideoCapture) -> None:
    while True:
        ser.write(b'!')
        _wait_and_render(vid, .5)
        ser.write(b'.')
        _wait_and_render(vid, .5)


@contextlib.contextmanager
def _shh(ser: serial.Serial) -> Generator[None, None, None]:
    try:
        yield
    finally:
        ser.write(b'.')


def _avg_color(
        frame: numpy.ndarray,
        y: int,
        x: int,
) -> tuple[float, float, float]:
    sums = [0] * 3

    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            for i, v in enumerate(frame[y + dy][x + dx]):
                sums[i] += v

    return (sums[0] / 9, sums[1] / 9, sums[2] / 9)


def _distance(
        c1: tuple[float, float, float],
        c2: tuple[float, float, float],
) -> float:
    return sum((b - a) ** 2 for a, b in zip(c1, c2))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--serial', default=SERIAL_DEFAULT)
    args = parser.parse_args()

    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 768)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # average color
    # did it change significantly?
    # last refresh time (to open and close the map)

    with serial.Serial(args.serial, 9600) as ser, _shh(ser):
        t0 = time.monotonic()

        frame = _getframe(vid)
        py = int(len(frame) * 135 / 850)
        px_1 = int(len(frame[0]) * 480 / 1510)
        px_2 = int(len(frame[0]) * 520 / 1510)

        frame = _getframe(vid, guide=False)
        color_1 = _avg_color(frame, py, px_1)
        color_2 = _avg_color(frame, py, px_2)

        while True:
            if (time.monotonic() - t0) >= 3 * 60 + 5:
                print('-> menuing to prevent sleep')
                _press(ser, '-')
                _press(ser, 'B')
                _wait_and_render(vid, .5)
                t0 = time.monotonic()

            _wait_and_render(vid, .25)

            frame = _getframe(vid, guide=False)
            new_color_1 = _avg_color(frame, py, px_1)
            new_color_2 = _avg_color(frame, py, px_2)

            distance_1 = _distance(color_1, new_color_1)
            distance_2 = _distance(color_2, new_color_2)
            if distance_1 >= 1800 and distance_2 >= 1800:
                print(f'space time?! {distance_1=} {distance_2=}')
                _alarm(ser, vid)

            color_1 = new_color_1
            color_2 = new_color_2

    vid.release()
    cv2.destroyAllWindows()
    return 0


if __name__ == '__main__':
    exit(main())
