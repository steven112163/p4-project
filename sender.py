from argparse import ArgumentParser, Namespace
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import sendp
from header import IntHeader


def parse_arguments() -> Namespace:
    """
    Parse arguments from command line
    :return: arguments
    """
    parser = ArgumentParser()
    parser.add_argument('-src', '--source', help="Source IP", type=str, default='10.0.0.1')
    parser.add_argument('-dst', '--destination', help='Destination IP', type=str, default='10.0.0.2')
    parser.add_argument('-if', '--interface', help='Name of the interface', type=str, default='h1-eth0')
    parser.add_argument('-c', '--count', help='Number of packets to be sent', type=int, default=1)

    return parser.parse_args()


if __name__ == '__main__':
    """
    Main function
        command: python3 sender.py [-src srcIP] [-dst dstIP] [-if interface] [-c count]
    """
    # Parse arguments
    args = parse_arguments()
    src_ip = args.source
    dst_ip = args.destination
    interface = args.interface
    count = args.count

    # Send packets
    packet = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(op=1, psrc=src_ip, pdst=dst_ip) / IntHeader()
    packet.show()
    sendp(packet, iface=interface, count=count)
