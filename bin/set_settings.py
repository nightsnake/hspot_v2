#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# HSpot provision module
# Will set settings: WG, Proxy, FW, WiFi, mac_access, user profiles
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
from blacklist import setProxy
from wg import setWG
from wifi import setWiFi
from user_profiles import setUserProfile
from mac_access import setIpBinding

def setBlackLIst(hspot, logger):
#Must return 0 if OK
 status = setProxy(hspot, logger)
 return status

def setWalledGarden(hspot, logger):
#Must return 0 if OK
 status = setWG(hspot, logger)
 return status

def setFW(id):
 return 0

def setWireless(hspot, logger):
 status = setWiFi(hspot, logger)
 return status

def setMACAccess(hspot, logger):
 status = setIpBinding(hspot, logger)
 return status

def setProfile(hspot, logger):
 status = setUserProfile
 return 0

def setSettings(logger, id=0):
 """
 Set settings on device from DB
 """
 a = devAction()
 hspots = {}
 if id:
  hspots = [ a.devGetById(id) ]
 else:
  hspots = a.devGetAlive()

 for hspot in hspots:

  fw = setFW(hspot, logger)
  mac = setMACAccess(hspot, logger)
  profile = setProfile(hspot, logger)
  wifi = setWireless(hspot, logger)
  list = setBlackList(hspot, logger)
  cna = setWalledGarden(hspot, logger)

#All functions must return 1 (0 if error)
  if fw and mac and profile and wifi and list and cna:
   try: 
    a.devSetDone(hspot.id)
   except Exception as e:
    logger.warning("Unexpected error: %s" % e)
   else:
    continue
  
if __name__ == "__main__":
    if len(sys.argv) > 1:
     try:
#If HSPOT ID defined, set only on it
      id = sys.argv[1]
      logger = logger("hs-setter")
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
     setSettings(logger)
     sys.exit(1)

