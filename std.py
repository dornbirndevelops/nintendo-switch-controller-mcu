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


def _dim(frame: numpy.ndarray) -> tuple[int, int, int, int]:
    px = int(len(frame[0]) * 570 / 1510)
    py = int(len(frame) * 130 / 850)

    w = int(len(frame[0]) * 100 / 1510)
    h = int(len(frame) * 10 / 850)

    return (px, py, w, h)


def _getframe(vid: cv2.VideoCapture) -> numpy.ndarray:
    _, frame = vid.read()

    px, py, w, h = _dim(frame)

    cv2.rectangle(
        frame,
        (px, py),
        (px + w, py + h),
        (0, 0, 255),
        1,
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--serial', default=SERIAL_DEFAULT)
    args = parser.parse_args()

    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 768)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    with serial.Serial(args.serial, 9600) as ser, _shh(ser):
        t0 = None

        while True:
            if t0 is None or (time.monotonic() - t0) >= 3 * 60 + 5:
                print('-> menuing to prevent sleep')
                _press(ser, '-')
                _press(ser, 'B')
                _wait_and_render(vid, .5)
                t0 = time.monotonic()

            _wait_and_render(vid, .25)

            frame = _getframe(vid)
            px, py, w, h = _dim(frame)

            filtered = frame[py:py+h, px:px+w, :] > (200, 200, 200)
            whites = numpy.apply_along_axis(all, axis=2, arr=filtered).sum()
            if whites >= 10:
                print(f'space time?! {whites=}')
                _alarm(ser, vid)

    vid.release()
    cv2.destroyAllWindows()
    return 0


if __name__ == '__main__':
    exit(main())
