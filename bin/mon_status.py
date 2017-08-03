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
from db_access_points import *

from logger import *
from connector import *

def getStatus():
 hspots = []

 a = devAction()
 p = access_pointsAction()

 hspots = a.devGetAll()


 for hspot in hspots:
  status = 0
  ap_status = 0
  try:
   logger.debug("Hotspot ID: %s" % (hspot.id))
   c = connectDevice(hspot.ip, hspot.login, hspot.password, hspot.type, logger)
   if c != -1:
    status = 1    
    aps = p.getAPByHspotId(hspot.id)   
    for ap in aps:
     try:
      cap = connectDevice(ap.ip, ap.login, ap.password, ap.type, logger)
      if cap != -1:
       ap_status = 1
     except Exception as e:
      logger.warning("Can't connect to AP: %s" % e)
      ap_status = 0
     p.setApStatus(ap.id, status)
   else:
    logger.debug("Hotspot %s: host is down" % (hspot.id))
    status = 0
    aps = p.getAPByHspotId(hspot.id)
    for ap in aps:
     logger.warning("AP %s: host is down" % e)
     ap_status = 0
  except Exception as e:
   logger.warning("Can't connect to Hotspot: %s" % e)
   status = 0
  a.devSetStatus(hspot.id, status)

def main():
     getStatus()

if __name__ == "__main__":
    logger = logger("hs-monitor")
    sys.exit(main())

