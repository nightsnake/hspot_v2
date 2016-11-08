#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# mon_status.py -- check device status
# need to add in crontab
# Copyright (C) Snake, 2016
##----------------------------------------------------------------------

import os, sys, inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../lib")))
if cmd_subfolder not in sys.path:
 sys.path.insert(0, cmd_subfolder)
from db_devices import *
from logger import *
from connector import *

def getStatus():
 hspots = []

 a = devAction()
 p = access_pointsAction()

 hspots = a.devGetAll()

 status = 0
 ap_status = 0

 for hspot in hspots:
  try:
   logger.debug("Hotspot ID: " + id)
   c = connectDevice(hspot.ip, hspot.login, hspot.password, hspot.type, logger)
   status = 1
   aps = p.getAPByHspotId(hspot.id)
   for ap in aps:
    try:
     cap = connectDevice(ap.ip, ap.login, ap.password, ap.type, logger)
     ap_status = 1
    except Exception as e:
     logger.warning("Can't connect to device: %s" % e)
     ap_status = 0
    p.setApStatus(ap.id, status)
  except Exception as e:
   logger.warning("Can't connect to device: %s" % e)
   status = 0
  a.devSetStatus(hspot.id, status)

def main():
     getStatus()

if __name__ == "__main__":
    logger = logger("hs-generator")
    sys.exit(main())

