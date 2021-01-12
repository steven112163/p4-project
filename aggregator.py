import sys
import os
import matplotlib.pyplot as plt
from pandas import read_csv
from argparse import ArgumentParser, Namespace
from math import ceil

def aggregate(dir_name: str, num_of_pkt: int) -> None:
    """
    Aggregate the csv results in the given directory
    :param dir_name: name of the given directory
    :param num_of_pkt: number of packets sent in each round
    :return: None
    """
    # Aggregate all csv
    aggregation_result = dict()
    zero_serial_number_csv = dict()

    with os.scandir(dir_name) as directory:
        for file in directory:
            if file.path.endswith('.csv') and file.is_file():
                
                if file.name.partition('-')[1] != "":
                    host = file.name.partition('-')[0] # host the file belongs to
                    if aggregation_result.get(host) is None: # not exist -> create one
                        aggregation_result[host] = read_csv(file.path)
                    else :  # exist -> append to old one
                        part = read_csv(file.path)
                        aggregation_result[host] = aggregation_result[host].append(part, ignore_index=True)

                    # serial number
                    serial_number = file.name.partition('_')[2][0:-4]
                    if serial_number == '0':
                        zero_serial_number_csv[host] = read_csv(file.path)

    # Output aggregation file
    for key in aggregation_result.keys():
        if aggregation_result.get(key) is not None:
            aggregation_result[key].to_csv(f'{dir_name}/{key}_aggregation.csv', index=False)
'''
def aggregate(dir_name: str, num_of_pkt: int) -> None:
    """
    Aggregate the csv results in the given directory
    :param dir_name: name of the given directory
    :param num_of_pkt: number of packets sent in each round
    :return: None
    """
    # Aggregate all csv
    result = None
    with os.scandir(dir_name) as directory:
        for file in directory:
            if file.path.endswith('.csv') and file.is_file():
                if result is None:
                    result = read_csv(file.path)
                else:
                    part = read_csv(file.path)
                    result = result.append(part, ignore_index=True)

    if result is not None:
        del result['Time']

        # Write the result to a file
        info_log('Record the result')
        result.to_csv(f'{dir_name}/aggregation.csv', index=False)

        # Plot the aggregation
        info_log('Draw')
        num_of_rows = float(len(result.index)) / num_of_pkt
        count = result.groupby(['IDs'], as_index=False).count()
        count.rename(columns={'Num_of_switch': 'Count'}, inplace=True)
        count['Count'] = count['Count'] / num_of_rows
        fig, ax = plt.subplots()
        rects = ax.bar(count['IDs'], count['Count'])
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.3f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
        ax.set_yticks(range(0, ceil(max(count['Count'])) + 1))
        ax.set_ylabel('Average number of occurrences')
        ax.set_xlabel('Route')
        ax.set_title('Average occurrences vs. Route')
        fig.tight_layout()
        plt.show()
'''

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

    return parser.parse_args()


if __name__ == '__main__':
    """
    Main function
        command: python3 aggregator.py [-d name_of_the_directory] [-c num_of_packets]
    """
    # Parse arguments
    args = parse_arguments()
    name = args.directory
    c = args.count

    # Aggregate
    info_log('Start aggregator')
    aggregate(name, c)
