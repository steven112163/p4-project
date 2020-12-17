from argparse import ArgumentParser, Namespace
from scapy.layers.l2 import ARP
from scapy.sendrecv import sniff
from datetime import datetime
import sys


def sniffer(name_of_interface: str) -> None:
    """
    Sniffer sniffing ARP packets
    :param name_of_interface: name of the interface to be sniffed
    :return: None
    """
    sniff(lfilter=lambda pkt: ARP in pkt, iface=name_of_interface, prn=lambda x: handler(x))


def handler(pkt):
    """
    Handler dealing with captured ARP requests
    :return: information about the request
    """
    return pkt.summary()


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
