#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# HSpot checking module
# Will check settings: WG, Proxy, FW, WiFi, mac_access, user profiles
# Copyright 2016 (c) Snake, <snake@nixman.info> @night_snake
##----------------------------------------------------------------------

import os, sys, inspect, getopt

#cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../lib")))
#if cmd_subfolder not in sys.path:
# sys.path.insert(0, cmd_subfolder)

#from RosAPI import Core
from logger import *
from db_devices import *
from db_devices_properties import *
from db_blacklist import *
from base import *
from blacklist import checkProxy

def checkFW():
 pass

def checkWIFI():
 pass

def checkMACAccess():
 pass

def checkUserProfile():
 pass

if __name__ == "__main__":
      print "Only as a module"
      sys.exit()
