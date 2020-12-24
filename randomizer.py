import json
import sys
from random import randint
from argparse import ArgumentParser, Namespace, ArgumentTypeError


def randomize(version: int, random_mode: int) -> None:
    """
    Randomize the link delay between switches
    :param version: version of P4 architecture
    :param random_mode: 0 for equal link delay, 1 for worst case, 2 for random link delay
    :return: None
    """
    if not version:
        # Version 1
        with open('p4app.json.txt') as in_file:
            data = json.load(in_file)

            # Random mode
            if random_mode == 2:
                # Randomize
                links = data['topology']['links']
                info_log('Random version 1')
                for idx, link in enumerate(links):
                    if idx < 4:
                        continue
                    link[2]['delay'] = f'{randint(0, 100)}ms'
            elif random_mode == 0:
                # Equal delay
                links = data['topology']['links']
                info_log('Equal delay version 1')
                for idx, link in enumerate(links):
                    if idx < 4:
                        continue
                    link[2]['delay'] = '10ms'
            else:
                # Worst case
                info_log('Worst case version 1')

            with open('p4app.json', 'w') as out_file:
                json.dump(data, out_file)
    else:
        # Version 2
        with open('p4app.json.txt') as in_file:
            data = json.load(in_file)
            data['program'] = 'project_v2.p4'
            for value in data['topology']['switches'].values():
                value['program'] = 'project_v2.p4'

            # Random mode
            if random_mode == 2:
                # Randomize
                info_log('Random version 2')
                links = data['topology']['links']
                for idx, link in enumerate(links):
                    if idx < 4:
                        continue
                    link[2]['delay'] = f'{randint(0, 100)}ms'
            elif random_mode == 0:
                # Equal delay
                links = data['topology']['links']
                info_log('Equal delay version 2')
                for idx, link in enumerate(links):
                    if idx < 4:
                        continue
                    link[2]['delay'] = '10ms'
            else:
                # Worst case
                info_log('Worst case version 2')

            with open('p4app.json', 'w') as out_file:
                json.dump(data, out_file)


def check_version_range(value: str) -> int:
    """
    Check if version argument is either 0 or 1
    :param value: string value
    :return: integer value
    """
    int_value = int(value)
    if int_value != 0 and int_value != 1:
        raise ArgumentTypeError(f'"{value}" is an invalid version. It should be 0 or 1.')

    return int_value


def check_random_range(value: str) -> int:
    """
    Check if random argument is either 0, 1 or 2
    :param value: string value
    :return: integer value
    """
    int_value = int(value)
    if int_value != 0 and int_value != 1 and int_value != 2:
        raise ArgumentTypeError(f'"{value}" is an invalid random mode. It should be 0, 1 or 2.')

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
    parser.add_argument('-v', '--version', help='Version of the P4 architecture', type=check_version_range, default=0)
    parser.add_argument('-r', '--random', help='Randomize or not', type=check_random_range, default=0)

    return parser.parse_args()


if __name__ == '__main__':
    """
    Main function
        command: python3 randomizer.py [-v (0-1)] [-r (0-2)]
    """
    # Parse arguments
    args = parse_arguments()
    ver = args.version
    ran = args.random

    # Randomize p4app.json
    randomize(ver, ran)
