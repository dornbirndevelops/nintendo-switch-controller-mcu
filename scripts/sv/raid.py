from __future__ import annotations

import argparse
import functools
import os.path

import cv2
import numpy
import serial

from scripts.engine import all_match
from scripts.engine import always_matches
from scripts.engine import Color
from scripts.engine import do
from scripts.engine import getframe
from scripts.engine import match_px
from scripts.engine import match_text
from scripts.engine import Point
from scripts.engine import Press
from scripts.engine import require_tesseract
from scripts.engine import run
from scripts.engine import SERIAL_DEFAULT
from scripts.engine import Wait


RAID_STRIPE_POS = Point(y=98, x=664)


def _extract_type(
        im: numpy.ndarray,
        dims: tuple[int, int, int],
) -> numpy.ndarray:
    im = cv2.resize(im, (dims[1], dims[0]))

    top_left = Point(y=68, x=604).norm(dims)
    bottom_right = Point(y=131, x=657).norm(dims)
    crop = im[top_left.y:bottom_right.y, top_left.x:bottom_right.x]

    color = numpy.array([71, 51, 39])
    t = numpy.array([1, 1, 1])
    return cv2.inRange(crop, color - t * 20, color + t * 20)


@functools.lru_cache
def _get_type_images(
        dims: tuple[int, int, int],
) -> tuple[tuple[str, numpy.ndarray], ...]:
    types_dir = os.path.join(os.path.dirname(__file__), 'types')

    return tuple(
        (tp, _extract_type(cv2.imread(os.path.join(types_dir, tp)), dims))
        for tp in os.listdir(types_dir)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--serial', default=SERIAL_DEFAULT)
    args = parser.parse_args()

    require_tesseract()

    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 768)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    raid_color = Color(-1, -1, -1)

    def _raid_appeared(vid: cv2.VideoCapture, ser: serial.Serial) -> None:
        nonlocal raid_color

        Wait(1)(vid, ser)

        frame = getframe(vid)

        px = frame[RAID_STRIPE_POS.norm(frame.shape)]
        raid_color = Color(b=int(px[0]), g=int(px[1]), r=int(px[2]))

        type_images = _get_type_images(frame.shape)

        tp_im = _extract_type(frame, frame.shape)
        _, tp = max(((im == tp_im).mean(), fname) for fname, im in type_images)
        print(f'the type is {tp}')

        # TODO: select pokemon based on type
        Press('A')(vid, ser)

    def _raid_color_gone(frame: numpy.ndarray) -> bool:
        return not match_px(RAID_STRIPE_POS, raid_color)(frame)

    states = {
        'INITIAL': (
            (
                match_px(Point(y=399, x=696), Color(b=17, g=203, r=244)),
                do(Wait(1), Press('X'), Wait(1), Press('d'), Wait(.5)),
                'MENU',
            ),
        ),
        'MENU': (
            (
                match_px(Point(y=230, x=700), Color(b=29, g=184, r=210)),
                do(Wait(1), Press('A')),
                'WAIT_FOR_PORTAL',
            ),
            (always_matches, do(Press('s'), Wait(.5)), 'MENU'),
        ),
        'WAIT_FOR_PORTAL': (
            (
                match_px(Point(y=451, x=115), Color(b=29, g=163, r=217)),
                # model takes a while to load
                Wait(5),
                'PORTAL',
            ),
        ),
        'PORTAL': (
            (
                match_px(Point(y=210, x=200), Color(b=22, g=198, r=229)),
                do(Wait(1), Press('A')),
                'WAIT_FOR_RAID_SELECT',
            ),
            (always_matches, do(Press('s'), Wait(.5)), 'PORTAL'),
        ),
        'WAIT_FOR_RAID_SELECT': (
            (
                match_px(
                    Point(y=451, x=115),
                    Color(b=156, g=43, r=133),  # violet
                    Color(b=33, g=98, r=197),  # scarlet
                ),
                Wait(1),
                'RAID_SELECT',
            ),
        ),
        'RAID_SELECT': (
            # TODO: later we can select based on disabled button
            (
                always_matches,
                do(
                    Press('a'), Wait(.4),
                    Press('s'), Wait(.4),
                    Press('A'), Wait(.4),
                ),
                'WAIT_FOR_RAID',
            ),
        ),
        'WAIT_FOR_RAID': (
            (
                all_match(
                    match_px(Point(y=398, x=394), Color(b=49, g=43, r=30)),
                    match_text(
                        "You weren't able to join.",
                        Point(y=352, x=211),
                        Point(y=398, x=394),
                        invert=True,
                    ),
                ),
                do(Wait(.5), Press('B'), Wait(.5), Press('A')),
                'WAIT_FOR_RAID',
            ),
            (
                match_px(
                    RAID_STRIPE_POS,
                    Color(b=211, g=108, r=153),  # violet
                    Color(b=60, g=82, r=217),  # scarlet
                    Color(b=134, g=99, r=86),  # 6 star
                    Color(b=20, g=184, r=227),  # event
                ),
                _raid_appeared,
                'RAID_ACCEPTED',
            ),
        ),
        'RAID_ACCEPTED': (
            (
                all_match(
                    match_px(Point(y=393, x=432), Color(b=49, g=43, r=30)),
                    match_text(
                        'The raid has been abandoned!',
                        Point(y=363, x=210),
                        Point(y=393, x=432),
                        invert=True,
                    ),
                ),
                do(Press('B'), Wait(1), Press('A')),
                'WAIT_FOR_RAID',
            ),
            (_raid_color_gone, Wait(5), 'RAID'),
        ),
        'RAID': (
            (
                match_px(Point(y=361, x=740), Color(b=21, g=180, r=208)),
                do(Press('A'), Wait(.2)),
                'RAID',
            ),
            (
                all_match(
                    match_px(Point(y=356, x=488), Color(b=244, g=237, r=220)),
                    match_px(Point(y=271, x=713), Color(b=31, g=183, r=200)),
                ),
                do(Wait(.3), Press('R'), Wait(.3), Press('A'), Wait(.3)),
                'RAID',
            ),
            (
                match_px(Point(y=271, x=713), Color(b=31, g=183, r=200)),
                do(Press('A'), Wait(.2)),
                'RAID',
            ),
            (
                match_px(Point(y=79, x=410), Color(b=26, g=207, r=228)),
                do(Press('A'), Wait(.2)),
                'RAID',
            ),
            # TODO: match the catch pokemon text here instead of 3 pts
            (
                all_match(
                    *(
                        match_px(p, Color(b=23, g=182, r=208))
                        for p in (
                            Point(y=402, x=678),
                            Point(y=402, x=738),
                            Point(y=402, x=748),
                        )
                    ),
                ),
                do(Wait(.5), Press('s'), Wait(.5), Press('A'), Wait(8)),
                'WAIT_FOR_SUCCESS',
            ),
            (
                all_match(
                    match_px(Point(y=381, x=515), Color(b=152, g=152, r=146)),
                    match_px(Point(y=5, x=5), Color(b=234, g=234, r=234)),
                    match_text(
                        'You and the others were blown out of the cavern!',
                        Point(y=353, x=111),
                        Point(y=380, x=457),
                        invert=True,
                    ),
                ),
                Wait(10),
                'INITIAL',
            ),
        ),
        'WAIT_FOR_SUCCESS': (
            (
                match_px(
                    Point(y=115, x=674),
                    Color(b=211, g=108, r=153),  # violet
                    Color(b=60, g=82, r=217),  # scarlet
                    Color(b=114, g=85, r=76),  # 6 star
                    Color(b=64, g=191, r=229),  # event
                ),
                do(Wait(1), Press('A'), Wait(10)),
                'INITIAL',
            ),
        ),
    }

    with serial.Serial(args.serial, 9600) as ser:
        run(vid=vid, ser=ser, initial='INITIAL', states=states)


if __name__ == '__main__':
    raise SystemExit(main())
