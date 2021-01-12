import sys
import os
from time import time
from pandas import DataFrame, read_csv
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
        info_log('Got ARP request from IP: {}, MAC: {}, {}'.format(pkt[ARP].psrc, pkt[ARP].hwsrc, elapsed_time))
        arp = pkt[ARP]
        if Padding in arp:
            int_header = IntHeader(bytes(arp[Padding]))
            info_log('Traverse {} switch(es) with id(s): {}\n'.format(int_header.len, int_header.id))

            # Get file number
            global number
            if not number > -1:
                number = 0
                filename = '../results/{}_{}.csv'.format(name_of_interface, number)
                while os.path.exists(filename):
                    number += 1
                    filename = '../results/{}_{}.csv'.format(name_of_interface, number)
            else:
                filename = '../results/{}_{}.csv'.format(name_of_interface, number)

            # Store the result
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

    # Set file number
    number = -1

    # Start sniffer
    info_log('{}'.format(datetime.now()))
    info_log('Start sniffer on interface {}. Quit the sniffer with CONTROL-C.\n'.format(interface))
    sniffer(interface)
