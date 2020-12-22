import json
import sys
from random import randint
from argparse import ArgumentParser, Namespace, ArgumentTypeError


def randomize(version: int, random_or_not: int) -> None:
    """
    Randomize the link delay between switches
    :param version: version of P4 architecture
    :param random_or_not: random or not
    :return: None
    """
    if not version:
        # Version 1
        with open('p4app.json.txt') as in_file:
            data = json.load(in_file)

            # Random or not
            if random_or_not:
                # Randomize
                links = data['topology']['links']
                info_log('Random version 1')
                for idx, link in enumerate(links):
                    if idx < 4:
                        continue
                    link[2]['delay'] = f'{randint(0, 100)}ms'
            else:
                info_log('Nonrandom version 1')

            with open('p4app.json', 'w') as out_file:
                json.dump(data, out_file)
    else:
        # Version 2
        with open('p4app.json.txt') as in_file:
            data = json.load(in_file)
            data['program'] = 'project_v2.p4'
            for value in data['topology']['switches'].values():
                value['program'] = 'project_v2.p4'

            # Random or not
            if random_or_not:
                # Randomize
                info_log('Random version 2')
                links = data['topology']['links']
                for idx, link in enumerate(links):
                    if idx < 4:
                        continue
                    link[2]['delay'] = f'{randint(0, 100)}ms'
            else:
                info_log('Nonrandom version 2')

            with open('p4app.json', 'w') as out_file:
                json.dump(data, out_file)


def check_int_range(value: str) -> int:
    """
    Check if argument is either 0 or 1
    :param value: string value
    :return: integer value
    """
    int_value = int(value)
    if int_value != 0 and int_value != 1:
        raise ArgumentTypeError(f'"{value}" is an invalid value. It should be 0 or 1')

    return int_value


def info_log(log: str) -> None:
    """
    Print logs
    :param log: log to be displayed
    :return: None
    """
    print(f'[\033[96mINFO\033[00m] {log}')
    sys.stdout.flush()


def parse_arguments() -> Namespace:
    """
    Parse arguments from command line
    :return: arguments
    """
    parser = ArgumentParser()
    parser.add_argument('-v', '--version', help='Version of the P4 architecture', type=check_int_range, default=0)
    parser.add_argument('-r', '--random', help='Randomize or not', type=check_int_range, default=0)

    return parser.parse_args()


if __name__ == '__main__':
    """
    Main function
        command: python3 randomizer.py [-v (0-1)] [-r (0-1)]
    """
    # Parse arguments
    args = parse_arguments()
    ver = args.version
    ran = args.random

    # Randomize p4app.json
    randomize(ver, ran)
