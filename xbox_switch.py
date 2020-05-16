from signal import pause
from xbox360controller import Xbox360Controller
from serial import Serial
from time import sleep
from math import ceil

STICK_MIN = 0x00
STICK_CENTER = 0x80
STICK_MAX = 0xff

DPAD_TOP = 0x00
DPAD_TOP_RIGHT = 0x01
DPAD_RIGHT = 0x02
DPAD_BOTTOM_RIGHT = 0x03
DPAD_BOTTOM = 0x04
DPAD_BOTTOM_LEFT = 0x05
DPAD_LEFT = 0x06
DPAD_TOP_LEFT = 0x07
DPAD_CENTER = 0x08

# values to pass into button functions
Y = (1, 0x01)
B = (1, 0x02)
A = (1, 0x04)
X = (1, 0x08)
L = (1, 0x10)
R = (1, 0x20)
ZL = (1, 0x40)
ZR = (1, 0x80)
MINUS = (0, 0x01)
PLUS = (0, 0x02)
LCLICK = (0, 0x04)
RCLICK = (0, 0x08)
HOME = (0, 0x10)
CAPTURE = (0, 0x20)

# values to pass into stick functions
L_STICK = (3, 4)
R_STICK = (5, 6)
L_LEFT = (3, STICK_MIN)
L_RIGHT = (3, STICK_MAX)
L_UP = (4, STICK_MIN)
L_DOWN = (4, STICK_MAX)
R_LEFT = (5, STICK_MIN)
R_RIGHT = (5, STICK_MAX)
R_UP = (6, STICK_MIN)
R_DOWN = (6, STICK_MAX)

dpad_positions = (
    (
        DPAD_BOTTOM_LEFT,
        DPAD_LEFT,
        DPAD_TOP_LEFT,
    ),
    (
        DPAD_BOTTOM,
        DPAD_CENTER,
        DPAD_TOP,
    ),
    (
        DPAD_BOTTOM_RIGHT,
        DPAD_RIGHT,
        DPAD_TOP_RIGHT,
    ),
)

# serial connection
serial = Serial('/dev/ttyS0')

# state command (default all neutral)
state = bytearray([0x0, 0x0, 0x0, 0x80, 0x80, 0x80, 0x80, 0x0])

# Button H (MINUS, PLUS, LCLICK, RCLICK, HOME, CAPTURE)
0x0,
# Button L (Y, B, A, X, L, R, ZL, ZR)
0x0,
# HAT (not modified)
0x8,
# LX
STICK_CENTER,
# LY
STICK_CENTER,
# RX
STICK_CENTER,
# RY
STICK_CENTER,
# VendorSpec (not modified)
0x0


_a = -1
_b = 1
_a2 = STICK_MIN
_b2 = STICK_MAX


def transform(v):
    return ceil(((v - _a) / (_b - _a)) * (_b2 - _a2) + _a2)


def button_press(button):  # works
    state[button[0]] |= button[1]
    serial.write(state)


def button_release(button):  # works
    state[button[0]] &= ~button[1]
    serial.write(state)


def move_trigger(rawaxis, trigger):  # works but inaccurate
    if rawaxis.value > 0.5:
        button_press(trigger)
    else:
        button_release(trigger)


def move_dpad(axis):  # works but with side-effect
    # neutral position is not recognized by driver
    # therefore send the neutral command after sending the registered command
    state[2] = dpad_positions[axis.x+1][axis.y+1]
    serial.write(state)
    sleep(1 / 60)
    state[2] = DPAD_CENTER
    serial.write(state)


def move_stick(axis, stick):  # works but inaccurate
    state[stick[0]] = transform(round(axis.x))
    state[stick[1]] = transform(round(axis.y))
    serial.write(state)


try:
    with Xbox360Controller(0) as controller:
        # with Xbox360Controller(0, axis_threshold=0.5) as controller:
        # Axis
        # Sticks
        controller.axis_l.when_moved = lambda a: move_stick(a, L_STICK)
        controller.axis_r.when_moved = lambda a: move_stick(a, R_STICK)

        # DPAD
        controller.hat.when_moved = lambda a: move_dpad(a)

        # Raw Axis
        # Trigger
        controller.trigger_l.when_moved = lambda ra: move_trigger(ra, ZL)
        controller.trigger_r.when_moved = lambda ra: move_trigger(ra, ZR)

        # Buttons
        # are mapped to the switch button layout
        controller.button_b.when_pressed = lambda b: button_press(A)
        controller.button_b.when_released = lambda b: button_release(A)
        controller.button_a.when_pressed = lambda b: button_press(B)
        controller.button_a.when_released = lambda b: button_release(B)
        controller.button_y.when_pressed = lambda b: button_press(X)
        controller.button_y.when_released = lambda b: button_release(X)
        controller.button_x.when_pressed = lambda b: button_press(Y)
        controller.button_x.when_released = lambda b: button_release(Y)
        controller.button_trigger_l.when_pressed = lambda b: button_press(L)
        controller.button_trigger_l.when_released = lambda b: button_release(L)
        controller.button_trigger_r.when_pressed = lambda b: button_press(R)
        controller.button_trigger_r.when_released = lambda b: button_release(R)
        controller.button_mode.when_pressed = lambda b: button_press(HOME)
        controller.button_mode.when_released = lambda b: button_release(HOME)
        controller.button_select.when_pressed = lambda b: button_press(MINUS)
        controller.button_select.when_released = lambda b: button_release(
            MINUS)
        controller.button_start.when_pressed = lambda b: button_press(PLUS)
        controller.button_start.when_released = lambda b: button_release(PLUS)
        controller.button_thumb_l.when_pressed = lambda b: button_press(LCLICK)
        controller.button_thumb_l.when_released = lambda b: button_release(
            LCLICK)
        controller.button_thumb_r.when_pressed = lambda b: button_press(RCLICK)
        controller.button_thumb_r.when_released = lambda b: button_release(
            RCLICK)

        pause()
except KeyboardInterrupt:
    pass
