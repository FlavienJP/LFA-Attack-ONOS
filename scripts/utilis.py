#!/usr/bin/python3
# Flavien JOLY POTTUZ / CNAM PARIS
# All rights reserved
# April 2020

from subprocess import call,check_output
import re, argparse
from time import sleep


def info():
    for switch in ["s1", "s2", "s3"]:
        cmd = check_output(["ovs-ofctl", "show", switch])
        switch_id = re.findall(r"\sLOCAL\(\S\d\):\saddr:(\S{2}:\S{2}:\S{2}:\S{2}:\S{2}:\S{2})", str(cmd))
        print(f"Switch {switch} : {switch_id[0]}")

def create():
    for switch in ["s1", "s2", "s3"]:
        call(["ovs-vsctl", "add-br", switch])
        call(["ovs-vsctl", "set", "bridge", switch, "protocols=OpenFlow10,OpenFlow11,OpenFlow12,OpenFlow13"])
        call(["ovs-vsctl", "set-controller", switch, "tcp:127.0.0.1:6633"])
    call(["ip", "netns", "add", "h1"])
    call(["ip", "netns", "add", "h2"])
    call(["ip", "netns", "add", "p1"])
    call(["ip", "netns", "add", "p2"])
    call(["ip", "link", "add", "h1-eth1", "type", "veth", "peer", "name", "s1-eth1"])
    call(["ip", "link", "add", "p1-eth1", "type", "veth", "peer", "name", "s1-eth2"])
    call(["ip", "link", "add", "h2-eth1", "type", "veth", "peer", "name", "s3-eth1"])
    call(["ip", "link", "add", "p2-eth1", "type", "veth", "peer", "name", "s3-eth2"])
    call(["ip", "link", "add", "s1-s2", "type", "veth", "peer", "name", "s2-s1"])
    call(["ip", "link", "add", "s2-s3", "type", "veth", "peer", "name", "s3-s2"])
    call(["ip", "link", "set", "h1-eth1", "netns", "h1"])
    call(["ip", "link", "set", "h2-eth1", "netns", "h2"])
    call(["ip", "link", "set", "p1-eth1", "netns", "p1"])
    call(["ip", "link", "set", "p2-eth1", "netns", "p2"])
    call(["ovs-vsctl", "add-port", "s1", "s1-eth1"])
    call(["ovs-vsctl", "add-port", "s1", "s1-eth2"])
    call(["ovs-vsctl", "add-port", "s1", "s1-s2"])
    call(["ovs-vsctl", "add-port", "s2", "s2-s1"])
    call(["ovs-vsctl", "add-port", "s2", "s2-s3"])
    call(["ovs-vsctl", "add-port", "s3", "s3-s2"])
    call(["ovs-vsctl", "add-port", "s3", "s3-eth1"])
    call(["ovs-vsctl", "add-port", "s3", "s3-eth2"])
    call(["ip", "netns", "exec", "h1", "ifconfig", "h1-eth1", "10.10.10.1/24"])
    call(["ip", "netns", "exec", "h1", "ifconfig", "lo", "up"])
    call(["ip", "netns", "exec", "h2", "ifconfig", "h2-eth1", "10.10.10.2/24"])
    call(["ip", "netns", "exec", "h2", "ifconfig", "lo", "up"])
    call(["ip", "netns", "exec", "p1", "ifconfig", "p1-eth1", "up"])
    call(["ip", "netns", "exec", "p2", "ifconfig", "p2-eth1", "up"])
    call(["ifconfig", "s1-eth1", "up"])
    call(["ifconfig", "s1-eth2", "up"])
    call(["ifconfig", "s3-eth1", "up"])
    call(["ifconfig", "s3-eth2", "up"])
    call(["ifconfig", "s1-s2", "up"])
    call(["ifconfig", "s2-s3", "up"])
    call(["ifconfig", "s2-s1", "up"])
    call(["ifconfig", "s3-s2", "up"])
    sleep(10)
    print("Ping test ... Please wait while we are validating the topology configuration...")
    call(["ip", "netns", "exec", "h1", "ping", "-c", "5", "10.10.10.2"])
    print("If ping is successful, you can continue. Please find below information about vswitchs :")
    info()

def clean():
    for switch in ["s1", "s2", "s3"]:
        call(["ovs-vsctl", "del-br", switch])
    for host in ["h1", "h2", "p1", "p2"]:
        call(["ip", "netns", "del", host])
    for host in ["s1-s2", "s2-s3"]:
        call(["ip", "link", "del", host])
    call(["service", "onos", "restart"])

def swap():
    clean()
    call(["service", "onos", "stop"])
    cmd = check_output(["ls", "-ln", "/opt"])
    actual_version = re.findall(r"onos\s->\s/opt/onos-1.(\d+).0", str(cmd))
    call(["rm", '/opt/onos',])
    if int(actual_version[0]) == 14:
        print("Change ONOS version from 1.14.0 to 1.15.0")
        call(["ln", "-s", '/opt/onos-1.15.0', "/opt/onos"])
    if int(actual_version[0]) == 15:
        print("Change ONOS version from 1.15.0 to 1.14.0")
        call(["ln", "-s", '/opt/onos-1.14.0', "/opt/onos"])
    call(["service", "onos", "start"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--info", action='store_true', help="Print OVS infos")
    parser.add_argument("--create", action='store_true', help="Create s1,s2 and s3 and connect to c1")
    parser.add_argument("--clean", action='store_true', help="Delete s1,s2 and s3, reload c1 to wipe config")
    parser.add_argument("--swap", action='store_true', help="Swap ONOS versions")

    args = parser.parse_args()
    if args.info :
        info()
    if args.create:
        create()
    if args.clean:
        clean()
    if args.swap:
        swap()

