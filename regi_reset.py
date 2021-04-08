from __future__ import annotations

import argparse
import time

import cv2
import numpy
import serial


def _press(ser: serial.Serial, s: str, duration: float = .1) -> None:
    ser.write(s.encode())
    time.sleep(duration)
    ser.write(b'0')
    time.sleep(.075)


def _getframe(vid: cv2.VideoCapture) -> numpy.ndarray:
    _, frame = vid.read()
    cv2.imshow('game', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        raise SystemExit(0)
    return frame


def _wait_and_render(vid: cv2.VideoCapture, t: float) -> None:
    end = time.time() + t
    while time.time() < end:
        _getframe(vid)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--serial', default='/dev/ttyUSB0')
    args = parser.parse_args()

    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 768)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    with serial.Serial(args.serial, 9600) as ser:
        while True:
            _press(ser, 'H')
            _wait_and_render(vid, 1)
            _press(ser, 'X')
            _wait_and_render(vid, 1)
            _press(ser, 'A')
            # TODO: we could notice the dialog quicker here
            _wait_and_render(vid, 3.5)
            _press(ser, 'A')
            _wait_and_render(vid, 1)
            _press(ser, 'A')

            frame = _getframe(vid)
            while not numpy.array_equal(frame[5][5], [16, 16, 16]):
                frame = _getframe(vid)

            print('startup screen!')

            frame = _getframe(vid)
            while numpy.array_equal(frame[5][5], [16, 16, 16]):
                frame = _getframe(vid)

            print('after startup!')
            _wait_and_render(vid, .5)
            _press(ser, 'A')

            frame = _getframe(vid)
            while not numpy.array_equal(frame[5][5], [16, 16, 16]):
                frame = _getframe(vid)

            frame = _getframe(vid)
            while numpy.array_equal(frame[5][5], [16, 16, 16]):
                frame = _getframe(vid)

            print('game loaded')
            _wait_and_render(vid, .5)
            _press(ser, 'A')
            _wait_and_render(vid, .5)
            _press(ser, 'A')
            _wait_and_render(vid, .75)
            _press(ser, 'A')

            frame = _getframe(vid)
            while not numpy.array_equal(frame[420][696], [59, 59, 59]):
                frame = _getframe(vid)

            print('dialog started')

            frame = _getframe(vid)
            while numpy.array_equal(frame[420][696], [59, 59, 59]):
                frame = _getframe(vid)

            print('dialog ended')
            t0 = time.time()

            frame = _getframe(vid)
            while not numpy.array_equal(frame[420][696], [59, 59, 59]):
                frame = _getframe(vid)

            print('dialog second time')
            t1 = time.time()

            print(f'dialog delay: {t1 - t0:.3f}s')

            if (t1 - t0) > 1:
                print('SHINY!!!')
                while True:
                    ser.write(b'!')
                    _wait_and_render(vid, .5)
                    ser.write(b'.')
                    _wait_and_render(vid, .5)

    vid.release()
    cv2.destroyAllWindows()
    return 0


if __name__ == '__main__':
    exit(main())
