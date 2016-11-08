#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# mon_user.py -- count wifi users on each AP
# need to add in crontab
# Copyright (C) Snake, 2016
##----------------------------------------------------------------------

import os, sys, inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../lib")))
if cmd_subfolder not in sys.path:
 sys.path.insert(0, cmd_subfolder)
from connector import Core
from db_devices import *
from logger import *

def getCurrentUsers():
 hspots = []
 a = devAction()
 p = access_pointsAction()
 logger = logger("hs-monitor")
 hspots = a.devGetAlive()

 for hspot in hspots:
  try:
   logger.debug("Hotspot ID: " + id)
   aps = p.getAPByHspotId(hspot.id)
   for ap in aps:
    try:
     c = connectDevice(hspot.ip, hspot.login, hspot.password, hspot.type, logger)
     online = []
     online = c.response_handler(c.talk(["/interface/wireless/registration-table/print"]))
     p.setApOnline(ap.id, len(online))        
  except Exception as e:
   logger.warning("Can't connect to device: %s" % e)   
def main():
     getCurrentUsers()
if __name__ == "__main__":
    sys.exit(main())

