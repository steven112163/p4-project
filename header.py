from scapy.fields import ShortField
from scapy.packet import Packet


class IntHeader(Packet):
    name = "In-band Telemetry Header"
    fields_desc = [ShortField('id', 1)]
