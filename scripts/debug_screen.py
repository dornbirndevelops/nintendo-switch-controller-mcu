from __future__ import annotations

import cv2

from scripts.engine import Color
from scripts.engine import get_text
from scripts.engine import Point


def main() -> int:
    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 768)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    pos = Point(y=-1, x=-1)
    start: Point | None = None

    def cb(event: int, x: int, y: int, flags: object, param: object) -> None:
        nonlocal start, pos

        if event == cv2.EVENT_MOUSEMOVE:
            pos = Point(y=y, x=x)
        elif event == cv2.EVENT_LBUTTONDOWN:
            start = Point(y=y, x=x)
        elif event == cv2.EVENT_LBUTTONUP:
            assert start is not None
            start = start.denorm(frame.shape)
            end = Point(y=y, x=x).denorm(frame.shape)

            _, current = vid.read()
            if start == end:
                print(f'match_px({end}, {Color(*current[y][x])})')
            else:
                start, end = min(start, end), max(start, end)
                for invert in (True, False):
                    text = get_text(current, start, end, invert=invert)
                    print('match_text(')
                    print(f'    {text!r},')
                    print(f'    {start},')
                    print(f'    {end},')
                    print(f'    invert={invert},')
                    print(')')

            start = None

    cv2.namedWindow('game')
    cv2.setMouseCallback('game', cb)

    while True:
        _, frame = vid.read()

        if start is not None:
            cv2.rectangle(
                frame,
                (start.x, start.y),
                (pos.x, pos.y),
                Color(b=255, g=0, r=0),
                1,
            )

        cv2.imshow('game', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            raise SystemExit(0)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
