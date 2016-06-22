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

class logger():

# logging.basicConfig(format = u'%(levelname)-4s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'hotspot.log')
 def __init__(self, topic, loglevel):
  base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
  log_path = "../var/log/"
  self.topic = topic
  self.loglevel = loglevel
  logfile = os.path.join(base_dir, log_path)+topic+".log"
  logging.basicConfig(format = u'%(levelname)-4s [%(asctime)s] %(message)s', level = loglevel, filename = logfile)
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
    pass

if __name__ == "__main__":
    sys.exit(main())

