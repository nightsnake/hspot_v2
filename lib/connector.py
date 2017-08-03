#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Category: base functions
# Make ssh/api connect to devices and return pointer
# Copyright (C) Snake, 2016 http://nixman.info
##----------------------------------------------------------------------

import os, sys
from RosAPI import Core

def connectToMikrotik(ip, login, password, logger):
 logger.debug("[connectToMikrotik] Trying to connect to %s with %s %s" % (ip, login, password))
 try: 
  c = Core(ip)
  c.login (login, password)
 except Exception as e:
  logger.error("[connectToMikrotik] Can't connect to device: %s" % e)
  return -1
 else:
  return c

def connectDevice(ip, login, password, type, logger):
 c = ''
 logger.debug("[connectDevice] Trying to connect to %s with %s %s (type %s)" % (ip, login, password, type))
 try:
  if type == 'mkt':
   c = connectToMikrotik(ip, login, password, logger)
 except Exception as e:
  logger.error("[connectDevice] Can't connect to device: %s" % e)
  return -1
 else:
  return c
