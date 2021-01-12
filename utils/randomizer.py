import json
import sys
import os
from random import randint
from argparse import ArgumentParser, Namespace, ArgumentTypeError


def randomize(version: int, random_mode: int, num_of_switches: int) -> None:
    """
    Randomize the link delay between switches
    :param version: version of P4 architecture
    :param random_mode: 0 for equal link delay, 1 for worst case, 2 for random link delay
    :param num_of_switches: number of switches
    :return: None
    """
    with open('utils/p4app.json.txt') as in_file:
        data = json.load(in_file)
        # Check p4 version
        if not version:
            # Version 1
            p4_file_name = 'project.p4'
            info_log('Version 1')

        else:
            # Version 2
            p4_file_name = 'project_v2.p4'
            info_log('Version 2')

        # sx-commands.txt
        for i in range(num_of_switches):
            file_content = 'mc_mgrp_create 1\n'
            file_content += 'mc_node_create '
            for j in range(num_of_switches + 1):
                file_content += str(j)
                if j != num_of_switches:
                    file_content += ' '
                else:
                    file_content += '\n'
            file_content += 'mc_node_associate 1 0\n'
            for j in range(num_of_switches):
                file_content += 'table_add switch_id_table get_switch_id ' + str(j + 1) + " => " + str(i + 1) + '\n'
            file_content += 'table_add l2 add_myTtl_multicast ff:ff:ff:ff:ff:ff => ' + str(i + 1) + '\n'
            file_content += 'table_add host_table remove_myTtl 1 =>\n'
            filename = 'runtime_commands/s' + str(i + 1) + '-commands.txt'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w') as out_file:
                out_file.write(file_content)

        # Switch info
        data['program'] = p4_file_name
        for i in range(num_of_switches):
            sx = 's' + str(i + 1)
            data['topology']['switches'][sx] = {"cli_input": "./runtime_commands/" + sx + "-commands.txt",
                                                "program": p4_file_name}

        # Links between hosts and switches
        for i in range(num_of_switches):
            hx = 'h' + str(i + 1)
            sx = 's' + str(i + 1)
            data['topology']['links'].append([hx, sx])

        # Links between switches
        if random_mode == 2:
            # Randomize
            info_log('Random delay')
            links = data['topology']['links']
            for i in range(num_of_switches):
                for j in range(i + 1, num_of_switches):
                    sx1 = 's' + str(i + 1)
                    sx2 = 's' + str(j + 1)
                    links.append([sx1, sx2, {'delay': '{}ms'.format(randint(0, 100))}])
        elif random_mode == 0:
            # Equal delay
            info_log('Equal delay')
            links = data['topology']['links']
            for i in range(num_of_switches):
                for j in range(i + 1, num_of_switches):
                    sx1 = 's' + str(i + 1)
                    sx2 = 's' + str(j + 1)
                    links.append([sx1, sx2, {'delay': '10ms'}])
        else:
            # Worst case
            info_log('Worst case')
            # TODO

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
        raise ArgumentTypeError('"{}" is an invalid version. It should be 0 or 1.'.format(value))

    return int_value


def check_random_range(value: str) -> int:
    """
    Check if random argument is either 0, 1 or 2
    :param value: string value
    :return: integer value
    """
    int_value = int(value)
    if int_value != 0 and int_value != 1 and int_value != 2:
        raise ArgumentTypeError('"{}" is an invalid random mode. It should be 0, 1 or 2.'.format(value))

    return int_value


def check_number_range(value: str) -> int:
    """
    Check if number of switches is greater than 3
    :param value: string value
    :return: integer value
    """
    int_value = int(value)
    if int_value < 3:
        raise ArgumentTypeError('"{}" is an invalid random mode. It should be >= 3.'.format(value))

    return int_value


def info_log(log: str) -> None:
    """
    Print logs
    :param log: log to be displayed
    :return: None
    """
    print('[\033[96mINFO\033[00m] {}'.format(log))
    sys.stdout.flush()


def parse_arguments() -> Namespace:
    """
    Parse arguments from command line
    :return: arguments
    """
    parser = ArgumentParser()
    parser.add_argument('-v', '--version', help='Version of the P4 architecture', type=check_version_range, default=0)
    parser.add_argument('-r', '--random', help='Randomize or not', type=check_random_range, default=0)
    parser.add_argument('-n', '--number', help='Number of switches', type=check_number_range, default=3)

    return parser.parse_args()


if __name__ == '__main__':
    """
    Main function
        command: python3 randomizer.py [-v (0-1)] [-r (0-2)] [-n (>= 3)]
    """
    # Parse arguments
    args = parse_arguments()
    ver = args.version
    ran = args.random
    num = args.number

    # Randomize p4app.json
    randomize(ver, ran, num)
