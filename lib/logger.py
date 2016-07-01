#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# logger module
# Copyright (C) Snake, 2015
##----------------------------------------------------------------------

import os, sys
#cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../lib")))
#if cmd_subfolder not in sys.path:
# sys.path.insert(0, cmd_subfolder)
import logging	
from config import Config


class logger():

# logging.basicConfig(format = u'%(levelname)-4s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'hotspot.log')
 def __init__(self, topic, verbose=0):
  base_dir = os.getcwd()
#Load vars from config
  config = Config()
  log_cfg = config.getLogConfig()
  level = log_cfg['level']
###@ Need some better
  path = "../" + log_cfg['path']
  self.topic = topic

  if verbose:
   self.loglevel = logging.getLevelName('DEBUG')
  else:
   self.loglevel = logging.getLevelName(level.upper())

  logfile = os.path.join(base_dir, path)+topic+".log"
#  logging.setLevel(self.loglevel)
  logging.basicConfig(format = u'%(levelname)-4s [%(asctime)s] %(message)s', level=self.loglevel, filename = logfile)
#  level = logging.setLevel(loglevel)

 def debug(self, msg):
#  if level >= 10:
   logging.debug( msg )

 def info(self, msg):
#  if level >= 20:
   logging.info( msg )

 def warning(self, msg):
#  if level > 4:
   logging.warning( msg )

 def error(self, msg):
#  if level > 3:
   logging.error( msg )

 def critical(self, msg):
#  if level > 2:
   logging.critical( msg )

def main ():
###@ Need to change text to description about methods of class logger()
    print "Logging module by Snake (c) 2016"

if __name__ == "__main__":
    sys.exit(main())

