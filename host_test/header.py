from scapy.fields import IntField, ShortField, FieldListField
from scapy.packet import Packet


class IntHeader(Packet):
    name = "In-band Network Telemetry Header"
    fields_desc = [ShortField('proto', None),
                   ShortField('len', None),
                   FieldListField('id', [], IntField('', None), count_from=lambda p: p.len)]
