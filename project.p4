#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_MYTTL = 0x1212;
const bit<16> TYPE_ARP   = 0x0806;
const bit<8>  init_ttl   = (bit<8>) 255;

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> switchID_t;

#define num_of_switch 10

/* Header */

header ethernet_t {
  macAddr_t dst_addr;
  macAddr_t src_addr;
  bit<16> ether_type;
}

header myTtl_t {
  bit<16>     proto_id;
  switchID_t  swid;
  bit<8>      ttl;
}

struct metadata{
  switchID_t  swid;
}

struct headers{
  ethernet_t   ethernet;
  myTtl_t      myTtl;
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
      default: accept;
    }
  }

  state parse_myTtl {
    pkt.extract(hdr.myTtl);
    transition accept;
  }

}

/* Checksum Verification */
control MyVerifyChecksum(inout headers hdr, inout metadata meta){
  apply {  }
}

/* Ingress Processing */
control MyIngress(inout headers hdr, inout metadata meta, inout standard_metadata_t std_meta){

  register<bit<16>>(num_of_switch) port_reg;
  register<bit<8>> (num_of_switch) ttl_reg;

  action drop() {
    mark_to_drop(std_meta);
  }

  action forward(egressSpec_t port_num) {
    std_meta.egress_spec = port_num;
  }

  action multicast(){
    std_meta.mcast_grp = 1;
  }

  action get_switch_id(switchID_t swid) {
    meta.swid = swid;
  }

  action add_myTtl_and_multicast(switchID_t swid) {
    hdr.myTtl.setValid();
    hdr.myTtl.ttl = init_ttl;
    hdr.myTtl.swid = swid;
    hdr.myTtl.proto_id = hdr.ethernet.ether_type;
    hdr.ethernet.ether_type = TYPE_MYTTL;
    std_meta.mcast_grp = 1;
  }

  table switch_id_table {

    key = {
      hdr.myTtl.swid: exact;
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
      add_myTtl_and_multicast;
      drop;
      NoAction;
    }
    default_action = NoAction;

  }

  apply {

    if(hdr.myTtl.isValid()){

      hdr.myTtl.ttl = hdr.myTtl.ttl-1;
      
      bit<16> port;
      bit<8>  ttl;
      
      switch_id_table.apply(); // grab id info should must match entry

      port_reg.read(port, meta.swid);
      ttl_reg.read(ttl, meta.swid);

      if(hdr.myTtl.ttl<ttl){
        mark_to_drop(std_meta);
      }
      else if(hdr.myTtl.ttl==ttl && (bit<16>)std_meta.ingress_port != port ){
        mark_to_drop(std_meta);
      }
      else if( hdr.myTtl.swid == meta.swid){
        mark_to_drop(std_meta);
      }
      else{
         std_meta.mcast_grp = 1;
      }
    }
    else {
      l2.apply(); // not contain a ttl hdr -> forwarding table Match
    }
  }

}

/* Engress Processing */
control MyEgress(inout headers hdr, inout metadata meta, inout standard_metadata_t std_meta){

  action forward(egressSpec_t port_num) {
    std_meta.egress_spec = port_num;
  }

  action remove_myTtl_and_forward(egressSpec_t port_num) {
    std_meta.egress_spec = port_num;
    hdr.ethernet.ether_type = hdr.myTtl.proto_id;
    hdr.myTtl.setInvalid();
  }

  table host_table  {

    key = {
      hdr.ethernet.dst_addr: exact;
    }

    actions = {
      forward;
      remove_myTtl_and_forward;
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


