import sys
from argparse import ArgumentParser, Namespace, ArgumentTypeError
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import sendp
from header import IntHeader


def check_test_type(value: str) -> int:
    """
    Check argument test is either 0 or 1
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
    parser.add_argument('-src', '--source', help="Source IP", type=str, default='10.0.1.1')
    parser.add_argument('-dst', '--destination', help='Destination IP', type=str, default='10.0.2.2')
    parser.add_argument('-if', '--interface', help='Name of the interface', type=str, default='h1-eth0')
    parser.add_argument('-c', '--count', help='Number of packets to be sent', type=int, default=1)
    parser.add_argument('-t', '--test', help='Whether test variable length field', type=check_test_type, default=0)
    parser.add_argument('-i', '--id', help='IDs to be placed in variable length field', type=int, nargs='*',
                        default=[1])

    return parser.parse_args()


if __name__ == '__main__':
    """
    Main function
        command: python3 sender.py [-src srcIP] [-dst dstIP] [-if interface] [-c count] [-t (0-1)] [-i list_of_ids]
    """
    # Parse arguments
    args = parse_arguments()
    src_ip = args.source
    dst_ip = args.destination
    interface = args.interface
    count = args.count
    test = args.test
    ids = args.id

    # Send packets
    if test:
        info_log(f'INT ARP with ids: {ids}')
        packet = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(op=1, psrc=src_ip, pdst=dst_ip) / IntHeader(
            proto=int('0x0800', 16), len=len(ids), id=ids)
    else:
        info_log('Pure ARP')
        packet = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(op=1, psrc=src_ip, pdst=dst_ip)
    sendp(packet, iface=interface, count=count)
