#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_MYTTL = 0x1212;
const bit<16> TYPE_ARP   = 0x0806;
const bit<16> TYPE_INT   = 0x9487 ;

const bit<8>  INIT_TTL   = (bit<8>) 255;

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> switchID_t;

#define NUM_OF_SWITCHES 10
#define MAX_INT_HEADERS 20

/* Header */

header ethernet_t {
  macAddr_t dst_addr;
  macAddr_t src_addr;
  bit<16> ether_type;
}

header myTtl_t {
  bit<16>     proto_id;
  switchID_t  src_swid;
  bit<8>      ttl;
}

header int_count_t {
  bit<16>   proto_id;
  bit<16>   num_switches;
}

header int_header_t {
  switchID_t switch_id;
}

header arp_t {
  bit<16> htype;
  bit<16> ptype;
  bit<8>  hlen;
  bit<8>  plen;
  bit<16> oper;
  bit<48> sha;
  bit<32> spa;
  bit<48> tha;
  bit<32> tpa;
}

struct parser_metadata_t {
  bit<16> num_headers_remaining;
}


struct metadata{
  switchID_t  swid;
  parser_metadata_t  parser_metadata;
}

struct headers{
  ethernet_t   ethernet;
  arp_t        arp;
  myTtl_t      myTtl;
  int_count_t  int_count;
  int_header_t[MAX_INT_HEADERS] int_headers;
}

/* Parser */
parser MyParser(packet_in pkt, out headers hdr, inout metadata meta, inout standard_metadata_t smeta){

  state start {
    transition parse_ethernet;
  }

  state parse_ethernet {
    pkt.extract(hdr.ethernet);
    transition select(hdr.ethernet.ether_type) {
      TYPE_MYTTL: parse_myTtl;
      TYPE_ARP: parse_arp;
      default: accept;
    }
  }

  state parse_myTtl {
    pkt.extract(hdr.myTtl);
    transition select(hdr.myTtl.proto_id) {
      TYPE_ARP: parse_arp;
      default: accept;
    }
  }

  state parse_arp {
    pkt.extract(hdr.arp);
    transition select(hdr.arp.ptype) {
      TYPE_INT: parse_int;
      default: accept;
    }
  }

  state parse_int {
    pkt.extract(hdr.int_count);
    meta.parser_metadata.num_headers_remaining = hdr.int_count.num_switches;
    transition select(meta.parser_metadata.num_headers_remaining){
      0: accept;
      default: parse_int_headers;
    }
  }

  state parse_int_headers {
    pkt.extract(hdr.int_headers.next);
    meta.parser_metadata.num_headers_remaining = meta.parser_metadata.num_headers_remaining -1 ;
    transition select(meta.parser_metadata.num_headers_remaining){
      0: accept;
      default: parse_int_headers;
    }
  }

}

/* Checksum Verification */
control MyVerifyChecksum(inout headers hdr, inout metadata meta){
  apply {  }
}

/* Ingress Processing */
control MyIngress(inout headers hdr, inout metadata meta, inout standard_metadata_t std_meta){

  register<bit<9>> (NUM_OF_SWITCHES) port_reg;
  register<bit<8>> (NUM_OF_SWITCHES) ttl_reg;

  action drop() {
    mark_to_drop(std_meta);
  }

  action forward(egressSpec_t port_num) {
    std_meta.egress_spec = port_num;
  }

  action get_switch_id(switchID_t swid) {
    meta.swid = swid;
  }

  action add_myTtl_and_int_multicast() {
    // add ttl
    hdr.myTtl.setValid();
    hdr.myTtl.ttl = INIT_TTL;
    hdr.myTtl.src_swid = meta.swid;
    hdr.myTtl.proto_id = hdr.ethernet.ether_type;
    hdr.ethernet.ether_type = TYPE_MYTTL;
    // add int_count
    hdr.int_count.setValid();
    hdr.int_count.num_switches = (bit<16>)0;
    hdr.int_count.proto_id = hdr.arp.ptype;
    hdr.arp.ptype = TYPE_INT;
    // multicast
    std_meta.mcast_grp = 1;
  }

  action add_int_header(){

    hdr.int_count.num_switches = hdr.int_count.num_switches + 1;

    hdr.int_headers.push_front(1);
    hdr.int_headers[0].setValid();
    hdr.int_headers[0].switch_id = meta.swid;
  }

  table int_table {
    actions = {
       add_int_header;
    }
    default_action = add_int_header;
  }

  table switch_id_table {

    key = {
      hdr.myTtl.src_swid: exact;  // Useless match field
    }

    actions = {
      get_switch_id;
      drop;
      NoAction;
    }
    default_action = NoAction;

  }

  table l2 {

    key = {
      hdr.ethernet.dst_addr: exact;
    }
    
    actions = {
      forward;
      add_myTtl_and_int_multicast;
    }
    default_action = add_myTtl_and_int_multicast;

  }

  apply {

    switch_id_table.apply(); // grab id info should must match entry

    if(hdr.myTtl.isValid()){

      hdr.myTtl.ttl = hdr.myTtl.ttl-1;
      
      bit<9> port;
      bit<8>  ttl;

      port_reg.read(port, hdr.myTtl.src_swid);
      ttl_reg.read(ttl, hdr.myTtl.src_swid);

      if(hdr.myTtl.ttl<ttl){
        mark_to_drop(std_meta);
      }
      else if(hdr.myTtl.ttl==ttl && std_meta.ingress_port != port ){
        mark_to_drop(std_meta);
      }
      else if( hdr.myTtl.src_swid == meta.swid){
        mark_to_drop(std_meta);
      }
      else{
         port_reg.write(hdr.myTtl.src_swid, std_meta.ingress_port);
         ttl_reg.write(hdr.myTtl.src_swid, hdr.myTtl.ttl);
         std_meta.mcast_grp = 1;
      }
    }
    else {
      l2.apply(); // not contain a ttl hdr -> forwarding table Match
    }

    if( hdr.int_count.isValid() ) {
      int_table.apply();
    }
  }

}

/* Engress Processing */
control MyEgress(inout headers hdr, inout metadata meta, inout standard_metadata_t std_meta){

  action remove_myTtl_and_int() {
    hdr.ethernet.ether_type = hdr.myTtl.proto_id;
    hdr.myTtl.setInvalid();

    hdr.arp.ptype = hdr.int_count.proto_id;
    hdr.int_count.setInvalid();
    hdr.int_headers.pop_front(hdr.int_headers.size);
  }

  table host_table  {

    key = {
      std_meta.egress_port: exact;
    }

    actions = {
      remove_myTtl_and_int;
      NoAction;
    }
    default_action = NoAction;

  }

  apply {

    // if ingress port == egress port -> drop
    if (std_meta.ingress_port == std_meta.egress_port) {
      mark_to_drop(std_meta);
    }
    else{
      host_table.apply();
    }
  }
}

/* Checksum Update */
control MyComputeChecksum(inout headers hdr, inout metadata meta){
  apply {  }
}

/* Deparser */
control MyDeparser(packet_out packet, in headers hdr){
  apply{
    packet.emit(hdr.ethernet);
    packet.emit(hdr.myTtl);
    packet.emit(hdr.arp);
    packet.emit(hdr.int_count);
    packet.emit(hdr.int_headers);
  }
}

V1Switch(
  MyParser(),
  MyVerifyChecksum(),
  MyIngress(),
  MyEgress(),
  MyComputeChecksum(),
  MyDeparser()
) main;


