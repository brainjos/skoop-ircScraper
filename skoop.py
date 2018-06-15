#!/usr/bin/python3
import time
import json
import threading
import os
from ircConnect import *
from config import *

#ESTABLISH CONNECTION TO IRC:
irc = IRC(server, channel, botnick)
irc.connect()

#DEFINE TEMPORARY STORAGE OF MESSAGE CHAINS:
chains = {}

#RETRIEVE CURRENT JSON DATA:
data = {}
with open('chainlog.json', 'r') as jsonFile:
    data = json.load(jsonFile)
next_id = data["next_id"]

#MESSAGE CHAIN:
class Chain:
    def __init__(self, duration):
        self.start_time = time.time()
        self.duration = duration
        self.messages = []
    def add_message(self, name, message):
        self.messages.append(name + ': ' + message)
    def check_status(self):
        if time.time() - self.start_time > self.duration:
            return True
        else:
            return False

#TIMER FOR UPDATING ARCHIVE:
class timerInstance (threading.Thread):
    def __init__(self, delay, next_id):
        threading.Thread.__init__(self)
        self.delay = delay
        self.next_id = next_id
    def run(self):
        while 1:
            time.sleep(self.delay)
            self.next_id = update_archive(self.next_id)

#FUNCTION TO UPDATE ARCHIVE:
def update_archive(next_id):
    print('Archiving chains!')
    removeKeys = []
    for c in chains:
        if chains[c].check_status() == True:
            removeKeys.append(c)
    if not removeKeys:
        print('Done Archiving - no chains were archived')
    else:
        numArchived = len(removeKeys)
        with open('chainlog.json', 'w') as jsonFile:
            for k in removeKeys:
                data["chains"].append({ "id":next_id, "messages":chains[k].messages })
                next_id += 1
                data["next_id"] = next_id
                del chains[k]
            json.dump(data, jsonFile, indent = 4)
        print('Done Archiving -', numArchived, 'chains archived')
    return next_id

#INSTANCE TIMER
timer = timerInstance(archive_check_delay, next_id)
timer.start()

#main loop
while 1:
    name, message = irc.rec_message()
    #message from troy or eby -- add message to all current chains
    if name in helpers:
        print('message from helpers! adding to all chains.')
        for c in chains:
            c.add_message(name, message)
    #current chain exists from given user -- add message to chain
    elif name in chains:
        print('new comment from origin of a chain, adding message.')
        chains[name].add_message(name, message)
    #detect new question, if reference to keywords
    else:
        if any(kword in message for kword in keywords):
            if all(bword not in message for bword in blocklist):
                if all(user != name for user in blockusers):
                    print('new chain initialized.')
                    chains[name] = Chain(chain_duration)
                    chains[name].add_message(name, message)
