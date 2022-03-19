from __future__ import annotations

import cv2
import numpy


def _getframe(vid: cv2.VideoCapture) -> numpy.ndarray:
    _, frame = vid.read()
    cv2.imshow('game', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        raise SystemExit(0)
    return frame


def main() -> int:
    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        frame = _getframe(vid)

        if numpy.array_equal(frame[457][881], (16, 16, 16)):
            print('menu is open')

            if all(c >= 210 for c in frame[61][315]):
                print('5 star!')

            print(f'{frame[115, 70]=} {frame[115, 216]=}')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
