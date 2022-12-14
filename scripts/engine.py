from __future__ import annotations

import shutil
import subprocess
import sys
import time
from typing import NamedTuple
from typing import NoReturn
from typing import Protocol

import cv2
import numpy
import serial

SERIAL_DEFAULT = 'COM1' if sys.platform == 'win32' else '/dev/ttyUSB0'


def require_tesseract() -> None:
    if not shutil.which('tesseract'):
        raise SystemExit('need to install `tesseract-ocr`')


def getframe(vid: cv2.VideoCapture) -> numpy.ndarray:
    _, frame = vid.read()
    cv2.imshow('game', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        raise SystemExit(0)
    return frame


def press(ser: serial.Serial, s: str, duration: float = .05) -> None:
    print(f'{s=} {duration=}')
    ser.write(s.encode())
    time.sleep(duration)
    ser.write(b'0')
    time.sleep(.075)


def wait_and_render(vid: cv2.VideoCapture, t: float) -> None:
    end = time.monotonic() + t
    while time.monotonic() < end:
        getframe(vid)


class Point(NamedTuple):
    y: int
    x: int

    def norm(self, dims: tuple[int, int, int]) -> Point:
        return type(self)(
            int(self.y / NORM.y * dims[0]),
            int(self.x / NORM.x * dims[1]),
        )

    def denorm(self, dims: tuple[int, int, int]) -> Point:
        return type(self)(
            int(self.y / dims[0] * NORM.y),
            int(self.x / dims[1] * NORM.x),
        )


NORM = Point(y=480, x=768)


class Color(NamedTuple):
    b: int
    g: int
    r: int


class Matcher(Protocol):
    def __call__(self, frame: numpy.ndarray) -> bool: ...


class Action(Protocol):
    def __call__(
            self,
            vid: cv2.VideoCapture,
            ser: serial.Serial,
    ) -> None:
        ...


def always_matches(frame: object) -> bool:
    return True


def all_match(*matchers: Matcher) -> Matcher:
    def all_match_impl(frame: numpy.ndarray) -> bool:
        return all(matcher(frame) for matcher in matchers)
    return all_match_impl


def match_px(point: Point, *colors: Color) -> Matcher:
    def match_px_impl(frame: numpy.ndarray) -> bool:
        px = frame[point.norm(frame.shape)]
        for color in colors:
            if sum((c2 - c1) * (c2 - c1) for c1, c2 in zip(px, color)) < 2000:
                return True
        else:
            return False
    return match_px_impl


def get_text(
        frame: numpy.ndarray,
        top_left: Point,
        bottom_right: Point,
        *,
        invert: bool,
) -> str:
    tl_norm = top_left.norm(frame.shape)
    br_norm = bottom_right.norm(frame.shape)

    crop = frame[tl_norm.y:br_norm.y, tl_norm.x:br_norm.x]
    crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    _, crop = cv2.threshold(
        crop, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU,
    )
    if invert:
        crop = cv2.bitwise_not(crop)

    return subprocess.check_output(
        ('tesseract', '-', '-', '--psm', '7'),
        input=cv2.imencode('.png', crop)[1].tobytes(),
        stderr=subprocess.DEVNULL,
    ).strip().decode()


def match_text(
        text: str,
        top_left: Point,
        bottom_right: Point,
        *,
        invert: bool,
) -> Matcher:
    def match_text_impl(frame: numpy.ndarray) -> bool:
        return text == get_text(frame, top_left, bottom_right, invert=invert)
    return match_text_impl


def do(*actions: Action) -> Action:
    def do_impl(vid: cv2.VideoCapture, ser: serial.Serial) -> None:
        for action in actions:
            action(vid, ser)
    return do_impl


class Press(NamedTuple):
    button: str
    duration: float = .05

    def __call__(self, vid: cv2.VideoCapture, ser: serial.Serial) -> None:
        press(ser, self.button, duration=self.duration)


class Wait(NamedTuple):
    d: float

    def __call__(self, vid: cv2.VideoCapture, ser: serial.Serial) -> None:
        wait_and_render(vid, self.d)


def run(
        *,
        vid: cv2.VideoCapture,
        ser: serial.Serial,
        initial: str,
        states: dict[str, tuple[tuple[Matcher, Action, str], ...]],
        transition_timeout: int = 420,
) -> NoReturn:
    t0 = time.monotonic()
    state = initial

    while True:
        frame = getframe(vid)

        for matcher, action, new_state in states[state]:
            if matcher(frame):
                action(vid, ser)
                if new_state != state:
                    print(f'=> {new_state}')
                    state = new_state
                    t0 = time.monotonic()
                break

        if time.monotonic() > t0 + transition_timeout:
            raise SystemExit(f'stalled in state {state}')
