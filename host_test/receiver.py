import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from time import time
from pandas import DataFrame, read_csv
from argparse import ArgumentParser, Namespace
from scapy.layers.l2 import Ether, ARP
from scapy.packet import Packet, Padding
from scapy.sendrecv import sniff
from datetime import datetime
from header import IntHeader
from math import ceil


def sniffer(name_of_interface: str) -> None:
    """
    Sniffer sniffing ARP packets
    :param name_of_interface: name of the interface to be sniffed
    :return: None
    """
    start_time = time()
    sniff(lfilter=lambda pkt: ARP in pkt, iface=name_of_interface,
          prn=lambda x: handler(x, name_of_interface, start_time))


def handler(pkt: Packet, name_of_interface: str, start_time: float) -> None:
    """
    Handler dealing with captured ARP requests
    :param pkt: packet received
    :param name_of_interface: name of the interface to be sniffed
    :param start_time: start time
    :return: None
    """
    elapsed_time = time() - start_time
    # Only process ARP requests
    if pkt[ARP].op == 1 and pkt[Ether].dst == 'ff:ff:ff:ff:ff:ff':
        info_log(f'Got ARP request from IP: {pkt[ARP].psrc}, MAC: {pkt[ARP].hwsrc}, {elapsed_time}')
        arp = pkt[ARP]
        if Padding in arp:
            int_header = IntHeader(bytes(arp[Padding]))
            info_log(f'Traverse {int_header.len} switch(es) with id(s): {int_header.id}\n')

            # Store the result
            filename = f'../results/{name_of_interface}.csv'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            ids = list(int_header.id)
            ids.reverse()
            new_entry = DataFrame([[int_header.len, ', '.join([str(i) for i in ids]), elapsed_time]],
                                  columns=['Num_of_switch', 'IDs', 'Time'])
            if os.path.exists(filename):
                result = read_csv(filename)
                result = result.append(new_entry, ignore_index=True)
                result.to_csv(filename, index=False)
            else:
                new_entry.to_csv(filename, index=False)

    return


def plot_the_result(name_of_interface: str) -> None:
    """
    Plot the result
    :param name_of_interface: name of the interface to be sniffed
    :return: None
    """
    # Read result file
    filename = f'../results/{name_of_interface}.csv'
    result = read_csv(filename)

    # Occurrences vs. Route
    count = result.groupby(['IDs'], as_index=False).count()
    count.rename(columns={'Num_of_switch': 'Count'}, inplace=True)
    plt.subplot(121)
    plt.bar(count['IDs'], count['Count'])
    plt.yticks(range(0, ceil(max(count['Count'])) + 1))
    plt.ylabel('The number of occurrences')
    plt.xlabel('Route')
    plt.title('Occurrences vs. Route')

    # Occurrence of the route vs. Time
    plt.subplot(122)
    result.sort_values(by=['Time'], inplace=True)
    minimum = min(result['Time'])
    x_coord = np.arange(minimum, max(result['Time']), 0.001, dtype=float)
    for i in result['IDs'].unique():
        selected = result[result['IDs'] == i]
        y_coord = np.zeros(x_coord.shape, dtype=int)
        for t in selected['Time']:
            y_coord[int((t - minimum) / 0.001)] = 1
        plt.plot(x_coord, y_coord, label=f'{i}')
    plt.legend()
    plt.yticks([0, 1], ['Not', 'Appear'])
    plt.ylabel('Appear or not')
    plt.xlabel('Time (s)')
    plt.title('Occurrences of the route vs. Time')

    plt.tight_layout()
    plt.show()


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
    parser.add_argument('-if', '--interface', help='Name of the interface', type=str, default='h2-eth0')

    return parser.parse_args()


if __name__ == '__main__':
    """
    Main function
        command: python3 receiver.py [-if interface]
    """
    # Parse arguments
    args = parse_arguments()
    interface = args.interface

    # Start sniffer
    info_log(f'{datetime.now()}')
    info_log(f'Start sniffer on interface {interface}. Quit the sniffer with CONTROL-C.\n')
    sniffer(interface)

    # Plot the result
    plot_the_result(interface)
