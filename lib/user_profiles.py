#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# module for checking hotspot user profiles
# Copyright (C) Snake, 2016 http://nixman.info
##----------------------------------------------------------------------

import os, sys, inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../lib")))
if cmd_subfolder not in sys.path:
 sys.path.insert(0, cmd_subfolder)

from db_devices import *
from logger import *
from db_user_profiles import *
from connector import *

# Set profile by profile ID
def setProfileById(profile_id):
 profile_string = "/ip/hotspot/user/profile/print"
 profile_set_string = "/ip/hotspot/user/profile/set"
 try:
  a = devAction()
  p = profileAction()

  hsid = p.getDeviceIdbyProfile(profile_id)
  hspot = a.devGetById(hsid)
  c = connectDevice(hspot.ip, hspot.login, hspot.password, hspot.type, logger)
  if(hspot.status):
   b_profile = p.getProfilebyID(profile_id)
   rate = b_profile.rate + " " + b_profile.rate + " " + "64k/64k" + " " + "5/5" + " 4 " + "64k/64k"
   profile = c.response_handler(c.talk([profile_string, "?name="+b_profile.name,]))
   result = c.response_handler(c.talk([profile_set_string, "=.id="+profile[0]['.id'],
                                                           "=session-timeout="+b_profile.session_timeout,
                                                           "=keepalive-timeout="+b_profile.dead_timeout,
                                                           "=idle-timeout="+b_profile.idle_timeout,
                                                           "=rate-limit="+rate]))
   return 1
  else:
   logger.warning("Device %s is offline, skipping..." % hspot.name)
   return 0

 except Exception as e:
  logger.error("Unexpected error: %s" % e)
  return -1

# Delete profile. Only by profile ID
# Not used now. Need to add another starting point
def delProfileById(profile_id, logger):
    hspots = []
    a = devAction()
    p = profileAction()
    try:
     hsid = p.getDeviceIdbyProfile(id)
     hspot = a.devGetById(hsid)
     if(hspot.status):
      c = connectDevice(hspot.ip, hspot.login, hspot.password, hspot.type, logger)  
      b_profile = p.getProfilebyID(id)
      profile = c.response_handler(c.talk(["/ip/hotspot/user/profile/print", "?name="+b_profile.name,]))
      c.response_handler(c.talk(["/ip/hotspot/user/profile/set", "=.id="+profile[0]['.id'], 
                                                                  "=session-timeout=1d",
                                                                  "=keepalive-timeout=2m",
                                                                  "=idle-timeout=none",
                                                                  "=rate-limit="+""]))
      return 1
     else:
      logger.warning("Device %s is offline, skipping..." % hspot.name)
      return 0
    except Exception as e:
     logger.error("Unexpected error: %s" % e)
     return -1

# Set profile by hspot ID (set all profiles for defined hspot)
def setUserProfile(hspot, logger):
 try:
  p = profileAction()
  profiles = p.getProfilesbyDevice(hspot.id)
  for profile in profiles: 
   status = setProfileById(profile.id)
   if status:
    return 1
  return 0
 except Exception as e:
  logger.error("Unexpected error: %s" % e)
  return -1 

if __name__ == "__main__":
###@Need to add help()
 print "Only as a module"
 sys.exit()
