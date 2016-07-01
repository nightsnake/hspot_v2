#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Connector
# Make ssh connects to devices and return pointer
# Copyright (C) Snake, 2016 http://nixman.info
##----------------------------------------------------------------------

import os, sys
from RosAPI import Core

def connectToMikrotik(ip, login, password):
 c = Core(ip)
 c.login (login, password)
 return c

def connectDevice(ip, login, password, type):
 if type eq 'mkt':
  c = connectToMikrotik(ip, login, password)
 return c
