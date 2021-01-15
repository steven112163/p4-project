import sys
import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import numpy as np
from pandas import read_csv, DataFrame
from argparse import ArgumentParser, Namespace
from math import ceil, floor, sqrt
from random import sample
from typing import Dict, List


def aggregate(dir_name: str, num_of_pkt: int, num_of_rounds: int) -> None:
    """
    Aggregate the csv results in the given directory
    :param dir_name: name of the given directory
    :param num_of_pkt: number of packets sent in each round
    :param num_of_rounds: number of rounds in each test
    :return: None
    """
    # Aggregate all csv
    aggregation_result = dict()
    zero_serial_number_csv = dict()
    pkt_in_each_test = dict()

    with os.scandir(dir_name) as directory:
        for file in directory:
            if file.path.endswith('.csv') and file.is_file():
                if file.name.partition('-')[1] != '':
                    result = read_csv(file.path)
                    host = file.name.partition('_')[0]  # which host the file belongs to
                    if aggregation_result.get(host) is None:  # not exist -> create one
                        aggregation_result[host] = result
                    else:  # exist -> append to old one
                        aggregation_result[host] = aggregation_result[host].append(result, ignore_index=True)

                    # serial number
                    serial_number = file.name.partition('_')[2][:-4]
                    if serial_number == '0':
                        zero_serial_number_csv[host] = result

                    # Get number of received packets in each test
                    if pkt_in_each_test.get(host) is None:
                        pkt_in_each_test[host] = {serial_number: len(result.index)}
                    else:
                        pkt_in_each_test[host][serial_number] = len(result.index)

    # Get number of rows/columns for display
    num_of_hosts = len(zero_serial_number_csv.keys())
    num_of_rows_or_cols = int(floor(sqrt(num_of_hosts)))

    # Get keys
    if num_of_rows_or_cols > 3:
        keys = get_sampled_keys(list(zero_serial_number_csv), 9)
        num_of_rows_or_cols = 3
    else:
        keys = get_sampled_keys(list(zero_serial_number_csv), num_of_rows_or_cols ** 2)

    # Draw the results of first test
    draw_first_results(zero_serial_number_csv, num_of_rows_or_cols, keys)

    # Draw aggregation results
    draw_aggregation(aggregation_result, num_of_rows_or_cols, keys, num_of_pkt, num_of_rounds)

    # Draw number of received packets in each test
    draw_pkt_in_each_round(pkt_in_each_test, num_of_rows_or_cols, keys)

    plt.show()


def get_sampled_keys(keys: List[str], num_of_keys: int) -> List[str]:
    """
    Get the requested number of keys
    :param keys: list of all keys
    :param num_of_keys: number of requested keys
    :return: sampled keys
    """
    sampled_keys = sample(keys, k=num_of_keys)
    sampled_keys.sort()
    sampled_keys.sort(key=len)

    return sampled_keys


def draw_first_results(zero_serial_number_csv: Dict[str, DataFrame], num_of_rows_or_cols: int, keys: List[str]) -> None:
    """
    Draw the results of first test with <= 9 hosts
    :param zero_serial_number_csv: first result of each host
    :param num_of_rows_or_cols: number of rows/columns for display
    :param keys: randomly sampled hosts to be displayed
    :return: None
    """
    for idx, key in enumerate(keys):
        fig = plt.figure()
        grid = gs.GridSpec(1, 2)
        result = zero_serial_number_csv[key]

        # Occurrences vs. Route
        ax = plt.Subplot(fig, grid[0])
        count = result.groupby(['IDs'], as_index=False).count()
        count.rename(columns={'Num_of_switch': 'Count'}, inplace=True)
        rects = ax.bar(count['IDs'], count['Count'])
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords='offset points',
                        ha='center',
                        va='bottom')

        ax.set_yticks(range(0, ceil(max(count['Count'])) + 3))
        ax.set_ylabel('Occurrences')
        ax.set_xlabel('Route')
        ax.set_title(f'{key}')
        fig.add_subplot(ax)

        # Occurrence of the route vs. Time
        ax = plt.Subplot(fig, grid[1])
        result.sort_values(by=['Time'], inplace=True)
        minimum = min(result['Time'])
        x_coord = np.arange(minimum, max(result['Time']), 0.001, dtype=float)
        for i in result['IDs'].unique():
            selected = result[result['IDs'] == i]
            y_coord = np.zeros(x_coord.shape, dtype=int)
            for t in selected['Time']:
                y_coord[int((t - minimum) / 0.001)] = 1
            ax.plot(x_coord, y_coord, label=f'{i}')
        ax.legend()
        ax.set_yticks([0, 1])
        ax.set_yticklabels(['F', 'T'])
        ax.set_ylabel('Appear or not')
        ax.set_xlabel('Time (s)')
        ax.set_title(f'{key}')
        fig.add_subplot(ax)

        fig.tight_layout()
        fig.canvas.set_window_title(f'First test of {key}')


def draw_aggregation(aggregation_result: Dict[str, DataFrame], num_of_rows_or_cols: int, keys: List[str],
                     num_of_pkt: int, num_of_rounds: int) -> None:
    """
    Draw the aggregation results
    :param aggregation_result: aggregation result of each host
    :param num_of_rows_or_cols: number of rows/columns for display
    :param keys: randomly sampled hosts to be displayed
    :param num_of_pkt: number of packets in each round
    :param num_of_rounds: number of rounds in each test
    :return: None
    """
    for idx, key in enumerate(keys):
        result = aggregation_result[key]
        del result['Time']

        # Plot the aggregation
        num_of_tests = float(len(result.index)) / num_of_pkt / num_of_rounds
        count = result.groupby(['IDs'], as_index=False).count()
        count.rename(columns={'Num_of_switch': 'Count'}, inplace=True)
        count['Count'] = count['Count'] / num_of_tests
        fig, ax = plt.subplots()
        rects = ax.bar(count['IDs'], count['Count'])
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
        ax.set_yticks(range(0, ceil(max(count['Count'])) + 3))
        ax.set_ylabel('Occurrences')
        ax.set_xlabel('Route')
        ax.set_title(f'{key}')
        fig.tight_layout()
        fig.canvas.set_window_title(f'Aggregation result of {key}')


def draw_pkt_in_each_round(pkt_in_each_round: Dict[str, Dict[str, int]], num_of_rows_or_cols: int, keys: List[str]) -> None:
    """
    Draw the number of received packets in each test
    :param pkt_in_each_round: number of received packets on each host in each round
    :param num_of_rows_or_cols: number of rows/columns for display
    :param keys: randomly sampled hosts to be displayed
    :return: None
    """
    fig = plt.figure()
    grid = gs.GridSpec(num_of_rows_or_cols, num_of_rows_or_cols)
    for idx, host in enumerate(keys):
        results = pkt_in_each_round[host]
        test_no = list(results.keys())
        test_no.sort()
        test_no.sort(key=len)

        values = [results[number] for number in test_no]

        ax = plt.Subplot(fig, grid[idx])
        rects = ax.bar(test_no, values)
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
        ax.set_yticks(range(0, ceil(max(values)) + 3))
        ax.set_ylabel('Packets')
        ax.set_xlabel('Test')
        ax.set_title(f'{host}')
        fig.add_subplot(ax)
    fig.tight_layout()
    fig.canvas.set_window_title('Received packets in each test')


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
    parser.add_argument('-d', '--directory', help='Name of the directory', type=str, default='results')
    parser.add_argument('-c', '--count', help='Number of packets sent in each round', type=int, default=5)
    parser.add_argument('-r', '--round', help='Number of rounds in each test', type=int, default=2)

    return parser.parse_args()


if __name__ == '__main__':
    """
    Main function
        command: python3 aggregator.py [-d name_of_the_directory] [-c num_of_packets] [-r num_of_rounds]
    """
    # Parse arguments
    args = parse_arguments()
    name = args.directory
    c = args.count
    r = args.round

    # Aggregate
    info_log('Start aggregator')
    aggregate(name, c, r)
