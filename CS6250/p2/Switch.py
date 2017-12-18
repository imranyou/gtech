# Project 2 for OMS6250
#
# This defines a Switch that can can send and receive spanning tree
# messages to converge on a final loop free forwarding topology.  This
# class is a child class (specialization) of the StpSwitch class.  To
# remain within the spirit of the project, the only inherited members
# functions the student is permitted to use are:
#
# self.switchID                   (the ID number of this switch object)
# self.links                      (the list of swtich IDs connected to this switch object)
# self.send_message(Message msg)  (Sends a Message object to another switch)
#
# Student code MUST use the send_message function to implement the algorithm -
# a non-distributed algorithm will not receive credit.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2016 Michael Brown, updated by Kelly Parks
#           Based on prior work by Sean Donovan, 2015

#### USED https://github.gatech.edu/iyousuf6/cs6250/blob/proj2/Project-2/Switch.py as I took this class before!

from Message import *
from StpSwitch import *

class Switch(StpSwitch):

    def remove_duplicates(results):
        someList = list(set(results))
        sort_someList = sorted(someList)
        return sort_someList

    def __init__(self, idNum, topolink, neighbors):
        # Invoke the super class constructor, which makes available to this object the following members:
        # -self.switchID                   (the ID number of this switch object)
        # -self.links                      (the list of swtich IDs connected to this switch object)
        super(Switch, self).__init__(idNum, topolink, neighbors)

        # switchID = id of the switch (lowest value determines root switcha nd breaks ties.)
    # topology = backlink to the Topology class. Used for sending messages.
    #   as follows: self.topology.send_message(message)
    # links = a list of the switch IDs linked to this switch.
        self.switchID = idNum
        self.topology = topolink
        self.links = neighbors
        self.root = self.switchID
        self.distance = 0

        self.spanning_tree = {link:[0,0,0] for link in self.links}


    def send_initial_messages(self):
        #TODO: This function needs to create and send the initial messages from this switch.

        # in the office hour it said only to use self.topology.send_message(message) and not self.topology.switches[neighbor].links
        for link in self.links:
            initialMessage = Message(self.switchID,0,self.switchID, link, True) # (claimedRoot, distanceToRoot, originID, destinationID)
            self.send_message(initialMessage)

    def send_new_message(self):
        for link in self.links:
            newMessage=Message(self.root, self.distance, self.switchID, link,False)
            self.send_message(newMessage)

    def check_if_equal(self,message):
        bufferAdd = 31
        if message.root == self.root:
            for link in self.spanning_tree.keys():
                if message.distance + bufferAdd < self.spanning_tree[link]:
                    self.spanning_tree[link] = -bufferAdd
                    self.spanning_tree[message.origin] = message.distance + bufferAdd
                    self.distance = message.distance + bufferAdd
                if message.distance + bufferAdd == self.spanning_tree[link]:
                    if message.origin < link:
                        self.spanning_tree[link] = -bufferAdd
                        self.spanning_tree[message.origin] = message.distance + bufferAdd
                if message.distance + bufferAdd > self.distance:
                    self.spanning_tree[message.origin] = -bufferAdd
                if message.distance + bufferAdd == self.spanning_tree[link] + bufferAdd:
                    self.spanning_tree[message.origin] == self.spanning_tree[message.origin]
                else:
                    self.send_initial_messages()


    def check_if_switch_is_less_than_message(self,message):
        bufferAdd = 31
        if message.root < self.root:
            self.root = message.root
            self.distance = message.distance + bufferAdd
            for link in self.spanning_tree:
                if link == message.origin:
                    self.spanning_tree[link] = message.distance + bufferAdd
                else:
                    self.spanning_tree[link] = -bufferAdd
            self.send_new_message()




    def process_message(self, message):
        self.check_if_switch_is_less_than_message(message)
        self.check_if_equal(message)




    def generate_logstring(self):
        logString = ""
        sortedRootSwitch = self.spanning_tree.keys()
        sortedWithoutRootSwitch = sorted(self.topology.switches)[1:]
        logString += (", ".join(str(min(self.topology.switches)) + " " +"-" + " " + str(x) for x in sortedRootSwitch)+"\n")


        for sw in sortedWithoutRootSwitch:
            bufferAdd = -1
            results = list()
            for l in self.topology.switches[sw].spanning_tree:
                if self.topology.switches[sw].spanning_tree[l] > bufferAdd:
                    results.append(l)
                if self.topology.switches[l].spanning_tree[sw] > bufferAdd:
                    results.append(l)
            new_result = set(results)
            logString += (", ".join(str(sw) + " " +"-" + " " + str(x) for x in sorted(list(new_result)))+"\n")
        return logString
