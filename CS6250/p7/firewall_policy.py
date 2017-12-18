#!/usr/bin/python
# CS 6250 Fall 2017 - Project 7 - SDN Firewall

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets
from pyretic.core import packet

def make_firewall_policy(config):
    # TODO - This is where you need to write the functionality to create the
    # firewall. The config is the firewall pol file that you created or as used in the
    # autograder.  PLEASE DO NOT HARD CODE FIREWALL RULES IN THIS FILE OR YOU WILL LOSE CREDIT.

    # This section is entirely optional, but some students will use this to define any data
    # structures needed outside of the config loop.

    # feel free to remove the following "print config" line once you no longer need it
    print config # for demonstration purposes only, so you can see the format of the config

    rules = []

    for entry in config:
        rule = match(ethtype=packet.IPV4)
        #print(rule)
        if entry['dstip'] != '-':
            rule &= match(dstip=IPAddr(entry['dstip']))
        #print(rule)

        if entry['srcport'] != '-':
            rule &= match(srcport=int(entry['srcport']))
        #print(rule)

        if entry['dstmac'] != '-':
            rule &= match(dstmac=EthAddr(entry['dstmac']))
        #print(rule)

        if entry['dstport'] != '-':
            rule &= match(dstport=int(entry['dstport']))
        #print(rule)

        if entry['protocol'] !='-':
            rule &= match(protocol=int(entry['protocol']))
        #print(rule)

        if entry['srcmac'] != '-':
            rule &= match(srcmac=EthAddr(entry['srcmac']))
        #print(rule)


        if entry['srcip'] != '-':
            rule &= match(srcip=IPAddr(entry['srcip']))
        #print(rule)

        else:
            rule=rule



        rules.append(rule)
        pass


    allowed = ~(union(rules))

    return allowed


def makeRule(dst):
    rule = match(ethtype=packet.IPV4)
    if dst['dstip'] != '-':
        rule &= match(dstip=IPAddr(dst['dstip']))
    if dst['srcport'] != '-':
        rule &= match(srcport=int(dst['srcport']))
    if dst['dstmac'] != '-':
        rule &= match(dstmac=EthAddr(dst['dstmac']))
    if dst['dstport'] != '-':
        rule &= match(dstport=int(dst['dstport']))
    if dst['protocol'] !='-':
        rule &= match(protocol=int(dst['protocol']))
    if dst['srcip'] != '-':
        rule &= match(srcip=IPAddr(dst['srcip']))
    if dst['srcmac'] != '-':
        rule &= match(srcmac=EthAddr(dst['srcmac']))
    else:
        rule=rule
    return rule
