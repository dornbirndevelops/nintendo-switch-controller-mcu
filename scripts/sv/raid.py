from __future__ import annotations

import argparse
import functools
import shutil
import subprocess
import sys
import time
from typing import Callable
from typing import Iterable
from typing import NamedTuple

import cv2
import numpy
import serial

SERIAL_DEFAULT = 'COM1' if sys.platform == 'win32' else '/dev/ttyUSB0'


class Point(NamedTuple):
    y: int
    x: int

    def norm(self, dims: Point) -> Point:
        return type(self)(
            int(self.y / NORM.y * dims.y),
            int(self.x / NORM.x * dims.x),
        )


NORM = Point(y=480, x=768)

# (b, g, r) because fuck cv2

MAP_CENTER = Point(y=399, x=696)
MAP_YELLOW = (17, 203, 244)

X_MENU_PORTAL_POS = Point(y=230, x=700)
X_MENU_YELLOW = (29, 184, 210)

PORTAL_RAID_POS = Point(y=210, x=200)
PORTAL_RAID_YELLOW = (22, 198, 229)

FOOTER_POS = Point(y=451, x=115)
RAID_FOOTER_PURPLE = (156, 43, 133)
PORTAL_FOOTER_YELLOW = (29, 163, 217)

RAID_STRIPE_POS = Point(y=98, x=664)
RAID_STRIPE_PURPLE = (211, 108, 153)
RAID_STRIPE_RED = (60, 82, 217)
RAID_STRIPE_6 = (134, 99, 86)


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

    return total < 2000


def _press(ser: serial.Serial, s: str, duration: float = .05) -> None:
    print(f'{s=} {duration=}')
    ser.write(s.encode())
    time.sleep(duration)
    ser.write(b'0')
    time.sleep(.075)


def _wait_and_render(vid: cv2.VideoCapture, t: float) -> None:
    end = time.time() + t
    while time.time() < end:
        _getframe(vid)


def _color_s(x: Iterable[int]) -> str:
    return ''.join(f'{n:02x}' for n in reversed(tuple(x)))


def _wait_for_colors(
        vid: cv2.VideoCapture,
        pos: Point,
        colors: tuple[tuple[int, int, int], ...],
        cb: Callable[[], None],
        *,
        timeout: int = 30,
) -> tuple[int, int, int]:
    end = time.monotonic() + timeout

    while True:
        px = _getframe(vid)[pos]
        if any(near_color(px, color) for color in colors):
            _wait_and_render(vid, 1)
            return (int(px[0]), int(px[1]), int(px[2]))
        elif time.monotonic() > end:
            raise SystemExit(
                f'failed to find expected color at {pos}\n\n'
                f'found: {_color_s(px)}\n'
                f'expected: {", ".join(_color_s(color) for color in colors)}',
            )
        else:
            cb()


def _extract_text(
        *,
        frame: numpy.ndarray,
        top_left: Point,
        bottom_right: Point,
        invert: bool,
) -> str:
    crop = frame[top_left.y:bottom_right.y, top_left.x:bottom_right.x]
    crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    _, crop = cv2.threshold(crop, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    if invert:
        crop = cv2.bitwise_not(crop)

    return subprocess.check_output(
        ('tesseract', '-', '-', '--psm', '7'),
        input=cv2.imencode('.png', crop)[1].tobytes(),
        stderr=subprocess.DEVNULL,
    ).strip().decode()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--serial', default=SERIAL_DEFAULT)
    parser.add_argument('--once', action='store_true')
    args = parser.parse_args()

    if not shutil.which('tesseract'):
        raise SystemExit('need to install `tesseract-ocr`')

    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 768)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    frame = _getframe(vid)
    dims = Point(y=len(frame), x=len(frame[0]))

    with serial.Serial(args.serial, 9600) as ser:
        while True:
            _wait_for_colors(
                vid=vid,
                pos=MAP_CENTER.norm(dims),
                colors=(MAP_YELLOW,),
                cb=functools.partial(_wait_and_render, vid, .2),
                # sometimes when losing this takes a while
                timeout=120,
            )

            _press(ser, 'X')
            _wait_and_render(vid, 1)

            def _press_key(key: str) -> None:
                _press(ser, key)
                _wait_and_render(vid, .5)

            # select poke portal
            _wait_for_colors(
                vid=vid,
                pos=X_MENU_PORTAL_POS.norm(dims),
                colors=(X_MENU_YELLOW,),
                cb=functools.partial(_press_key, 'w'),
            )

            _press(ser, 'A')

            _wait_for_colors(
                vid=vid,
                pos=FOOTER_POS.norm(dims),
                colors=(PORTAL_FOOTER_YELLOW,),
                cb=functools.partial(_wait_and_render, vid, .2),
            )

            # sometimes the model takes a while to load?
            _wait_and_render(vid, 5)

            # TODO: make sure we are online!

            # select tera raid battle
            _wait_for_colors(
                vid=vid,
                pos=PORTAL_RAID_POS.norm(dims),
                colors=(PORTAL_RAID_YELLOW,),
                cb=functools.partial(_press_key, 's'),
            )

            _press(ser, 'A')

            _wait_for_colors(
                vid=vid,
                pos=FOOTER_POS.norm(dims),
                colors=(RAID_FOOTER_PURPLE,),
                cb=functools.partial(_wait_and_render, vid, .2),
            )

            _press(ser, 'a')
            _wait_and_render(vid, .4)
            _press(ser, 's')
            _wait_and_render(vid, .4)
            _press(ser, 'A')

            # now wait for *either* red or purple
            raid_color = _wait_for_colors(
                vid=vid,
                pos=RAID_STRIPE_POS.norm(dims),
                colors=(
                    RAID_STRIPE_PURPLE,
                    RAID_STRIPE_RED,
                    RAID_STRIPE_6,
                ),
                cb=functools.partial(_wait_and_render, vid, .2),
            )

            _press(ser, 'A')

            # wait for raid color to fade out, then wait so we don't see map
            while True:
                raid_px = _getframe(vid)[RAID_STRIPE_POS.norm(dims)]
                if near_color(raid_px, raid_color):
                    _wait_and_render(vid, .2)
                else:
                    print('raid is starting!')
                    _wait_and_render(vid, 5)
                    break

            while True:
                frame = _getframe(vid)

                if near_color(
                        frame[Point(y=361, x=740).norm(dims)],
                        (21, 180, 208),
                ):
                    print('click [Battle]...')
                    _press(ser, 'A')
                    _wait_and_render(vid, .2)

                elif (
                        near_color(
                            frame[Point(y=356, x=488).norm(dims)],
                            (244, 237, 220),
                        )
                        and
                        near_color(
                            frame[Point(y=271, x=713).norm(dims)],
                            (31, 183, 200),
                        )
                ):
                    print('TERRA TIME...')
                    _press(ser, 'R')
                    _wait_and_render(vid, .3)
                    _press(ser, 'A')
                    _wait_and_render(vid, .3)

                elif near_color(
                        frame[Point(y=271, x=713).norm(dims)],
                        (31, 183, 200),
                ):
                    print('click move...')
                    _press(ser, 'A')
                    _wait_and_render(vid, .3)

                elif near_color(
                        frame[Point(y=79, x=410).norm(dims)],
                        (26, 207, 228),
                ):
                    print('click target...')
                    _press(ser, 'A')
                    _wait_and_render(vid, 1)

                elif all(
                        near_color(pt, (23, 182, 208))
                        for pt in (
                            frame[Point(y=402, x=678).norm(dims)],
                            frame[Point(y=402, x=738).norm(dims)],
                            frame[Point(y=402, x=748).norm(dims)],
                        )
                ):
                    print('skip catching...')
                    _press(ser, 's')
                    _wait_and_render(vid, .2)
                    _press(ser, 'A')
                    _wait_and_render(vid, 8)

                    # wait for success screen
                    _wait_for_colors(
                        vid=vid,
                        pos=Point(y=115, x=674).norm(dims),
                        colors=((211, 108, 153), (114, 85, 76)),
                        cb=functools.partial(_wait_and_render, vid, .2),
                    )

                    _press(ser, 'A')

                    break

                elif (
                        near_color(
                            frame[Point(y=381, x=515).norm(dims)],
                            (152, 152, 146),
                        )
                        and
                        near_color(
                            frame[Point(y=5, x=5).norm(dims)],
                            (234, 234, 234),
                        )
                        and
                        near_color(
                            frame[Point(y=50, x=50).norm(dims)],
                            (234, 234, 234),
                        )
                        and
                        _extract_text(
                            frame=frame,
                            top_left=Point(y=353, x=111).norm(dims),
                            bottom_right=Point(y=380, x=457).norm(dims),
                            invert=True,
                        ) == 'You and the others were blown out of the cavern!'
                ):
                    print('we lost :(...')
                    _wait_and_render(vid, 10)
                    break

            if args.once:
                return 0

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
