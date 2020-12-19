import sys
import os
import time
import pandas as pd
from argparse import ArgumentParser, Namespace
from scapy.layers.l2 import Ether, ARP
from scapy.packet import Packet, Padding
from scapy.sendrecv import sniff
from datetime import datetime
from header import IntHeader


def sniffer(name_of_interface: str) -> None:
    """
    Sniffer sniffing ARP packets
    :param name_of_interface: name of the interface to be sniffed
    :return: None
    """
    start_time = time.time()
    sniff(lfilter=lambda pkt: ARP in pkt, iface=name_of_interface,
          prn=lambda x: handler(x, name_of_interface, start_time))


def handler(pkt: Packet, name_of_interface: str, start_time: float) -> None:
    """
    Handler dealing with captured ARP requests
    :param pkt: packet received
    :param name_of_interface: name of the interface to be sniffed
    :param start_time: starting time of the sniffer
    :return: None
    """
    elapsed_time = time.time() - start_time
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
            new_entry = pd.DataFrame([[int_header.len, ', '.join([str(i) for i in int_header.id]), elapsed_time]],
                                     columns=['Num_of_switch', 'IDs', 'Time'])
            if os.path.exists(filename):
                result = pd.read_csv(filename)
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
    # TODO
    pass


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
    try:
        sniffer(interface)
    except KeyboardInterrupt:
        plot_the_result(interface)
