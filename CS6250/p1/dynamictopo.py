#!/usr/bin/python


# CS6250 Computer Networks Project 1
# Creates a dynamic topology based on command line parameters and starts the Mininet Command Line Interface.

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import lg, output, setLogLevel
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
import argparse
import sys
import os

# Parse Command Line Arguments
parser = argparse.ArgumentParser(description="Dynamic Topologies")
parser.add_argument('--delay',
                    help="Latency of network links, in ms",
                    required=True)

parser.add_argument('--bw',
                    type=int,
                    help=("Bandwidth of the links in Mbps."
                    "Must be >= 1"),
                    required=True)

parser.add_argument('--z',
                    type=int,
                    help=("Number of zones to create."
                    "Must be >= 1"),
                    required=True)

parser.add_argument('--n',
                    type=int,
                    help=("Number of hosts to create in each zone."
                    "Must be >= 1"),
                    required=True)

args = parser.parse_args()

lg.setLogLevel('info')

# Topology to be instantiated in Mininet
class DynamicTopo(Topo):
    "Dynamic Topology"

    def __init__(self, n=1, delay='1ms', z=1, bw=1, cpu=.1, max_queue_size=None, **params):
        """Ring topology with z zones.
           n: number of hosts per zone
           cpu: system fraction for each host
           bw: link bandwidth in Mb/s
           delay: link latency (e.g. 10ms)"""

        # Initialize topo
        Topo.__init__(self, **params)

        #TODO: Create your Dynamic Mininet Topology here!
        #NOTE: You MUST label switches as s1, s2, ... sz
        #NOTE: You MUST label hosts as h1-1, h1-2, ... hz-n
        #HINT: Use a loop to construct the topology in pieces.
        if n<1 or z<1:
            return -1
        hostConfig = {'cpu': cpu}
        linkConfig = {'bw': bw, 'delay': delay, 'max_queue_size': max_queue_size }

        s = []
        h = []

        for i in range(z):
            numOftheSwitch = 's%s' % (i+1)
            s.append(self.addSwitch(numOftheSwitch))
            if i>0:
                self.addLink(s[i-1],s[i], **linkConfig)
            for k in range(n):
                numOftheHost = 'h%s-%s' % ((i+1),(k+1))
                h.append(self.addHost(numOftheHost))
                self.addLink('s%s' % (i+1),numOftheHost, **linkConfig)


        #self.addLink(s[0],s[1], **linkConfig)
        #self.addLink(s[1],s[2], **linkConfig)
        #self.addLink(s[2],s[0], **linkConfig)








def main():
    "Create specified topology and launch the command line interface"
    topo = DynamicTopo(n=args.n, delay=args.delay, z=args.z, bw=args.bw)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()

    #TODO: Since this topology contains a cycle, we must enable the Spanning Tree Protocol (STP) on each switch.
    #      This is done with the following line of code: s1.cmd('ovs-vsctl set bridge s1 stp-enable=true')
    #      Here, you will need to generate this line of code for each switch.
    #HINT: You will need to get the switch objects from the net object defined above.

    #s=[]
    #for i in range(args.z):
        #numSwitch = 's%s' % (i+1)
        #s.append(numSwitch)

    for k in range(args.z):
        net.get('s%s' % (k+1)).cmd('ovs-vsctl set bridge ' + "s%s" % (k+1) + '  stp-enable=true')

    #net.pingAll()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    main()
