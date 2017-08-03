#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Category: setter, checker
# Will add/delete mac-address for bypass access (ip bindings)
# Copyright (C) Snake, 2016 http://nixman.info
##----------------------------------------------------------------------

import os, sys, inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../lib")))
if cmd_subfolder not in sys.path:
 sys.path.insert(0, cmd_subfolder)

from db_mac_users import *
from db_devices import *
from logger import *
from connector import *

def addUsers(id):
    hspots = []
    a = devAction()
    u = macAction()
    try:
     hsid = u.getDevicebyUser(id)
    except:
     print "Can't get information about HSPOT"
     exit()
    else:
     hspot = a.devGetById(hsid)
     if(hspot.status):
        user = u.getUserbyID(id)
        try:
            c = Core(hspot.ip)
            c.login (hspot.login, hspot.password)
            c.response_handler(c.talk(["/ip/hotspot/ip-binding/add", "=type="+"bypassed", "=mac-address="+user.mac_addr, "=comment="+str(id),]))
        except:
            print "Can't connect to" + hspot.ip
            status = 0

def setUsersById(id):
    hspots = []
    a = devAction()
    u = macAction()
    try:
#     print "Getting hspot ID for user " + id
     hsid = u.getDevicebyUser(id)
#     print "Hspot " + str(hsid) + " found"
    except:
     print "Can't get information about HSPOT"
     exit()
    else:
     hspot = a.devGetById(hsid)
     if(hspot.status):
#        print "Getting information about user..."
        user = u.getUserbyID(id)
        try:
            c = Core(hspot.ip)
            c.login (hspot.login, hspot.password)
            set_user = c.response_handler(c.talk(["/ip/hotspot/ip-binding/print", "?comment="+str(id),]))
            if set_user:
             c.response_handler(c.talk(["/ip/hotspot/ip-binding/set", "=.id="+set_user[0]['.id'], "=mac-address="+user.mac_addr, ]))
            else:
             print "User not found"
        except:
            print "Can't connect to" + hspot.ip
            status = 0

def delUsers(id):
    hspots = []
    a = devAction()
    u = macAction()
    try:
#     print "Getting hspot ID for user " + id
     hsid = u.getDevicebyUser(id)
#     print "Hspot " + str(hsid) + " found"
    except:
     print "Can't get information about HSPOT"
     exit()
    else:
     hspot = a.devGetById(hsid)
     if(hspot.status):
#        print "Getting information about user..."
        user = u.getUserbyID(id)
        try:
            c = Core(hspot.ip)
            c.login (hspot.login, hspot.password)
            user = c.response_handler(c.talk(["/ip/hotspot/ip-binding/print", "?comment="+str(id),]))
            c.response_handler(c.talk(["/ip/hotspot/ip-binding/remove", "=.id="+user[0]['.id'], ]))
        except:
            print "Can't connect to" + hspot.ip
            status = 0

# Set IP Bindings by hspot ID
def setIpBinding(hspot, logger):
 u = macAction()
 a = devAction()
###@Something strange... need to check deeply
 try:
  mac_users = u.getUsersbyDevice(hspot.id)
  for user in mac_users:
   status = setUsersById(user.id)
   if status:
    return 1
  return 0
 except Exception as e:
  logger.error("Unexpected error: %s" % e)
  return -1

if __name__ == "__main__":
###@Need to add help()
 print "Only as a module"
 sys.exit()
