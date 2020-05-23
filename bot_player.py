'''
play a bot script
'''
from argparse import ArgumentParser
from binascii import unhexlify
from serial import Serial
from time import sleep


class BotPlayer(object):
    def __init__(self, filename, device):
        self._device = device
        self._setup_commands = []
        self._loop_commands = []

        setup_read = False
        with open(filename, 'r') as file:
            for line in file:
                if len(line) == 1:
                    setup_read = True
                    continue

                # skip comments
                if line.startswith('#'):
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

        for iteration in range(number):
            self._loop()


def main(args):
    with BotPlayer(args.filename, args.device) as player:
        player.play(int(args.iterations))


if __name__ == "__main__":
    # creating a parser
    parser = ArgumentParser(
        description='play a bot script'
    )

    # adding arguments
    parser.add_argument(
        "--file", "-f",
        dest="filename",
        required=True,
        help="path to bot file containing the commands to play",
        metavar="filename",
    )

    parser.add_argument(
        "--serial", "-s",
        dest="device",
        required=True,
        help="where to send the bot commands to",
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
