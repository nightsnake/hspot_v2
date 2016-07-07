#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# module for checking WG settings
# Copyright 2016 (c) Snake, <snake@nixman.info> @night_snake
##----------------------------------------------------------------------

import os, sys, inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../lib")))
if cmd_subfolder not in sys.path:
 sys.path.insert(0, cmd_subfolder)

from db_devices_properties import *
from connector import *

def getCNASettings():
 pass

def setCNASettings():
 pass

def getSocialSettings():
 pass

def setSocialSettings():
 pass

def checkWG(hspot, logger):
 t = devices_propertiesAction()
 wg_social = []
 if hspot.status:
  try:
   # make connection to device (by api)
   c = connectDevice(hspot.ip, hspot.login, hspot.password, hspot.type, logger)

   # Load settings from DB
   wg = t.getSettingsById(hspot.id)

   # get status from device
   ###@ Need to load CNA settings from DB
   cna_apple, cna_android, cna_win = getCNASettings(c, logger)
   # Write settings to device
   ###@ Need to add DD-WRT support
   setCNASettings(cna_apple, cna_android, cna_win, wg, c)
   ###@ Need to load social settings from DB
   wg_social = getSocialSettings(c, logger)   
   # Write to device
   setSocialSettings(wg, wg_social, c, logger)

  except Exception as e:
   logger.error("Unexpected error: %s" % e)
   return 1
  else:
   return 0
 else:
  logger.waring("Device %s is offine. Skipping..." % hspot.name)
  return 1


if __name__ == "__main__":
 print "Only as a module"
 sys.exit()

