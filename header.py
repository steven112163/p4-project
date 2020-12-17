from scapy.fields import ShortField, FieldListField
from scapy.packet import Packet


class IntHeader(Packet):
    name = "In-band Network Telemetry Header"
    fields_desc = [ShortField('len', None),
                   FieldListField('id', [], ShortField('', None), count_from=lambda p: p.len)]
