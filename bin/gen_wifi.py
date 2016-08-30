#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# HSpot access points configurator
# Will set settings: SSID, password, frequency
# Copyright 2016 (c) Snake, <snake@nixman.info> @night_snake
##----------------------------------------------------------------------

import os, sys, inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../lib")))
if cmd_subfolder not in sys.path:
 sys.path.insert(0, cmd_subfolder)

from db_devices import *
from db_access_points import *
from logger import *
from wifi import *

def genApConfig(logger, id=0):
 aps = []
 a = devAction()
 p = access_pointsAction()
 if id:
  aps = [p.getAPById(id)]
 else:
  aps = p.getAPAlive()
 for ap in aps:
  if ap.status:
   try:
    done = setWiFi(ap, logger)
    p.setApDone(id, done)
#      else:
###need to set smth if error

   # Return 1 if OK
    return 1
   except Exception as e:
    logger.error("[genApConfig] Unexpected error: %s" % e)
    return -1
  else:
   logger.warning("[genApConfig] Device %s is offline, skipping...")


#Set WiFi AP settings by its ID
if __name__ == "__main__":
    if len(sys.argv) > 1:
     try:
#If AP ID defined, set only on it
      id = sys.argv[1]
      logger = logger("hs-ap-config")
      logger.debug("AP ID: " + id)
      genApConfig(logger, id)
     except Exception as e:
      logger.warning("[Main] Unexpected error: %s" % e)
      sys.stderr.write("Error: %s\n" % e)
      sys.exit(1)
     else:
      sys.exit(0)
    else:
#If AP ID not defined, check all hspots
     genApConfig(logger)
     sys.exit(1)

