#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# HSpot checking module
# Will check settings: WG, Proxy, FW, WiFi, mac_access, user profiles and would set flag "new" if check failed
# Copyright 2016 (c) Snake, <snake@nixman.info> @night_snake
##----------------------------------------------------------------------

import os, sys, inspect, getopt

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../lib")))
if cmd_subfolder not in sys.path:
 sys.path.insert(0, cmd_subfolder)

#from RosAPI import Core
from logger import *
from db_devices import *
from db_devices_properties import *
from db_blacklist import *
from base import *
from blacklist import checkProxy

def checkBlackLIst(hspot, logger):
 status = checkProxy(hspot, logger)
 return status

def checkFW(id):
 return 0

def checkWIFI(id):
 return 0

def checkMACAccess(id):
 return 0

def checkUserProfile(id):
 return 0

def checkSettings(logger, id=0):
 """
 Check settings on device
 """
 a = devAction()
 hspots = {}
 if id:
  hspots = [ a.devGetById(id) ]
 else:
# Get only hspots with changed settings
  hspots = a.devGetAlive()

 for hspot in hspots:
  fw = checkFW(hspot, logger)
  mac = checkMACAccess(hspot, logger)
  profile = checkUserProfile(hspot, logger)
  wifi = checkWIFI(hspot, logger)
  list = checkBlackList(hspot, logger)
  if fw or mac or profile or wifi or list:
   try: 
    a.devSetNew(hspot.id)
   except Exception as e:
    logger.warning("Unexpected error: %s" % e)
   else:
    continue
  
if __name__ == "__main__":
    if len(sys.argv) > 1:
     try:
#If HSPOT ID defined, set only on it
      id = sys.argv[1]
      logger = logger("hs-checker")
      logger.debug("Hotspot ID: " + id)
      setSettings(logger, id)
     except Exception as e:
      logger.warning("Unexpected error: %s" % e)
      sys.stderr.write("Error: %s\n" % e)
      sys.exit(1)
     else:
      sys.exit(0)
    else:
#If HSPOT ID not defined, check all hspots
     checkSettings(logger)
     sys.exit(1)

