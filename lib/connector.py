#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Connector
# Make ssh connects to devices and return pointer
# Copyright (C) Snake, 2016 http://nixman.info
##----------------------------------------------------------------------

import os, sys
from RosAPI import Core

def connectToMikrotik(ip, login, password, logger):
 try: 
  c = Core(ip)
  c.login (login, password)
 except Exception as e:
  logger.error("Can't connect to device: %s" % e)
  return 0
 else:
  return c

def connectDevice(ip, login, password, type, logger):
 c = ''
 try:
  if type eq 'mkt':
   c = connectToMikrotik(ip, login, password)
 except Exception as e:
  logger.error("Can't connect to device: %s" % e)
  return 0
 else:
  return c
