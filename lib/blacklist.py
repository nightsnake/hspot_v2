#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Category: setter, checker
# Will check settings: Blacklist (proxy settings)
# Copyright 2016 (c) Snake, <snake@nixman.info> @night_snake
##----------------------------------------------------------------------

from db_blacklist import *
from connector import *

def clearBlackList(c, logger):
 try:
  cur_list = c.response_handler(c.talk(["/ip/proxy/access/print"]))
  for entry in cur_list:
   c.response_handler(c.talk(["/ip/proxy/access/remove", "=.id="+entry['.id']]))
 except Exception as e:
  logger.error("Can't clear blacklist, Unexpected error: %s" % e)
  return -1
 else:
  return 0
 
def setBlackList(c, hspot, blacklist, logger):
 try:
  proxy = c.response_handler(c.talk(["/ip/proxy/set", "=always-from-cache=no",
                                                                 "=cache-administrator=webmaster",
                                                                 "=cache-hit-dscp=4",
                                                                 "=cache-on-disk=no",
                                                                 "=enabled=yes",
                                                                 "=max-cache-size=none",
                                                                 "=max-client-connections=600",
                                                                 "=max-fresh-time=3d",
                                                                 "=max-server-connections=600",
                                                                 "=parent-proxy=0.0.0.0",
                                                                 "=parent-proxy-port=0",
                                                                 "=port=3128",
                                                                 "=serialize-connections=no",
                                                                 "=src-address=0.0.0.0",]))
  for site in blacklist:
   c.response_handler(c.talk(["/ip/proxy/access/add", "=action=deny", "=disabled=no", "=dst-host="+site.site]))
 except Exception as e:
  logger.error("Can't fill up blacklist, Unexpected error: %s" % e)
  return -1
 else:
  return 0


def setProxy(hspot, logger):
 b = blacklistAction()

 if hspot.status:
  try:
   #Proxy settings (blacklist)
   blacklist = []
   blacklist = b.getSitesByDevId(hspot.id)
   # make connection to device (by api)
   c = connectDevice(hspot.ip, hspot.login, hspot.password, hspot.type, logger)
   # Clear blacklist (delete all entries)
   clearBlackList(c, logger)
   if blacklist:
    setBlackList(c, hspot, blacklist, logger)
  except Exception as e:
   logger.error("Unexpected error: %s" % e)
   return -1
  else:
   return 0
 else:
  logger.warning("Device %s is offine. Skipping..." % hspot.name)
  return 0

if __name__ == "__main__":
 print "Only as a module"
 sys.exit()


