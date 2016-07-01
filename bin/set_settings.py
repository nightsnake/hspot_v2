#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Device provisioning module
# Set settings from DB to HotSpot
# Copyright 2016 (c) Snake, <snake@nixman.info> @night_snake
##----------------------------------------------------------------------

import os, sys, inspect, getopt
import subprocess

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../lib")))
if cmd_subfolder not in sys.path:
 sys.path.insert(0, cmd_subfolder)

from logger import *
from string import Template
from config import Config
from db_devices import *
from base import *
from check_settings import *
#from check_proxy import *
#from check_wg import *


def setSettings(logger, id=0):
 """
 Set settings from database to device.
 """
 a = devAction()
 t = devices_propertiesAction()
 b = blacklistAction()
 hspots = {}
 if id:
  hspots = [ a.devGetById(id) ]
 else:
# Get only hspots with changed settings
  hspots = a.devGetAliveAndNew()

 for hspot in hspots:
   try:
#    checkSSID(hspot.id, logger)
#    checkProxy(hspot, logger)
#    checkWG(hspot.id, logger)
#    checkProfils(hspot.id, logger)
#    checkMAC(hspot.id, logger)
#    checkFW(hspot.id, logger)
   except Exception as e:
    logger.warning("Unexpected error for hspot %s (%s): %s" % (hspot.name, hspot.ip, e))
    print "Can't connect to device: %s" % hspot.ip


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
     sys.stdout.write("You have to define device id: %s <id>\n" % sys.argv[0])
     sys.exit(1)

