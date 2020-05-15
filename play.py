from pynput.keyboard import Listener, Key
from binascii import unhexlify
from time import sleep
from serial import Serial
import os.path


class CommandPlayer(object):
    def __init__(self, filename, device):
        self._device = device
        self._setup_commands = []
        self._loop_commands = []

        setup_read = False
        with open(filename, 'r') as file:
            for line in file:
                if len(line) == 0:
                    setup_read = True
                    continue

                raw, duration = line.split(' ')
                state = (unhexlify(raw.encode()), int(duration))
                if setup_read:
                    self._loop_commands.append(state)
                else:
                    self._setup_commands.append(state)

    def __enter__(self):
        self._serial = Serial(self._device)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._serial.close()

    def _setup(self):
        for command, duration in self._setup_commands:
            self._serial.write(command)
            sleep(duration / 1000)

    def _loop(self):
        for command, duration in self._loop_commands:
            self._serial.write(command)
            sleep(duration / 1000)

    def play(self, number):
        self._setup()

        while number == 0:
            self._loop()

        iteration = 0
        while iteration < number:
            self._loop()
            iteration += 1


def main(args):
    with CommandPlayer(args.filename, args.device) as cp:
        cp.play(int(args.iterations))


if __name__ == "__main__":
    from argparse import ArgumentParser

    # creating a parser
    parser = ArgumentParser(
        description='tool to play a series of input commands for the serial switch conroller'
    )

    # adding arguments
    parser.add_argument(
        "--file", "-f",
        dest="filename",
        required=True,
        help="where to play the commands from",
        metavar="filename",
    )

    parser.add_argument(
        "--serial", "-s",
        dest="device",
        required=True,
        help="where to send the commands to",
        metavar="device_adress",
    )

    parser.add_argument(
        "--iterations", "-i",
        dest="iterations",
        required=False,
        default="0",
        help="how often the loop should run",
        metavar="number",
    )

    # parse arguments
    args = parser.parse_args()

    # run main program
    main(args)
