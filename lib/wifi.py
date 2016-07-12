#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Category: setter, checker
# Will check settings: WiFi settings SSID, frequency, cipher
# Copyright (C) Snake, 2016 http://nixman.info
##----------------------------------------------------------------------

import os, sys, inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../lib")))
if cmd_subfolder not in sys.path:
 sys.path.insert(0, cmd_subfolder)
from db_devices import *
from db_devices_properties import *
from db_access_points import *
from connector import *

def setPassword(c, hspot, ap, logger):
 try:
 #Set settings for Mikrotik AP
  if ap.type eq 'mkt':
   profile_string = "/interface/wireless/security-profiles/print"
   profile_set_string = "/interface/wireless/security-profiles/set"
   profiles = c.response_handler(connect.talk([profile_string]))
   for profile in profiles:
#Check cipher settings and PSK
    if 'default' in profile['name']:
     if hspot.service_encryption and hspot.service_wifi:      
      p1 = connect.response_handler(connect.talk([profile_set_string, "=.id="+profile['.id'], 
                                                                                               "=wpa-pre-shared-key="+hspot.service_pass, 
                                                                                               "=wpa2-pre-shared-key="+hspot.service_pass,
                                                                                               "=mode=dynamic-keys", 
                                                                                               "=authentication-types=wpa-psk,wpa2-psk",
                                                                                               "=unicast-ciphers=tkip,aes-ccm", 
                                                                                               "=group-ciphers=tkip,aes-ccm",
                                                                                               ]))
     else:
      p1 = connect.response_handler(connect.talk([profile_set_string, "=.id="+profile['.id'],
                                                                                               "=mode=none",
                                                                                               "=authentication-types=",
                                                                                               "=unicast-ciphers=",
                                                                                               "=group-ciphers=",
                                                                                               "=wpa-pre-shared-key=",
                                                                                               "=wpa2-pre-shared-key=",

  return 0                                                                                               ]))      
 except Exception as e:
  logger.error("Unexpected error: %s" % e)
  return 1
#return passwd

def setSSID(c, hspot, ap, logger):
 wlans = []
 ssid = ''
 wifi_string = "/interface/wireless/print"
 #Set settings for Mikrotik AP
 try:
  if ap.type eq 'mkt':
   wlans = c.response_handler(c.talk([wifi_string]))
   for wlan in wlans:
   # Set hotspot AP, not service AP
    if 'hs-ap-' in wlan['name'] and not 'hs-ap-default' in wlan['name']:
     w = c.response_handler(c.talk(["/interface/wireless/set", "=.id="+wlan['.id'], "=ssid="+hspot.ssid, ]))
   #Set default mkt wifi adapter
    elif 'wlan1' in wlan['name'] or 'hs-ap-default' in wlan['name']:
     w = c.response_handler(c.talk(["/interface/wireless/set", "=.id="+wlan['.id'], "=ssid="+hspot.service_ssid, ]))
   ###@ Need to check
    hide-ssid = hspot.service_hide and "no" or "yes"      
    w = c.response_handler(c.talk(["/interface/wireless/set", "=.id="+wlan['.id'], "=hide-ssid="+hide-ssid, ]))
  return 0
 except Exception as e:
  logger.error("Unexpected error: %s" % e)
  return 1
#return ssid

def setFreq(c, ap, hspot):
 wifi_string = "/interface/wireless/print"
 #Set settings for Mikrotik AP
 try:
  if ap.type eq 'mkt':
   wlans = c.response_handler(c.talk([wifi_string]))
   for wlan in wlans:
   #Set default mkt wifi adapter
    if 'wlan1' in wlan['name'] or 'hs-ap-default' in wlan['name']:
     w = c.response_handler(c.talk(["/interface/wireless/set", "=.id="+wlan['.id'], "=frequency="+ap.freq, ]))
  return 0
 except Exception as e:
  logger.error("Unexpected error: %s" % e)
  return 1

#return freq

def setWiFi(hspot, logger):
 # Check not hspots, but access points
 a = devAction()
 t = devices_propertiesAction()
 p = access_pointsAction()

 aps = p.getAPByHspotId(hspot.id)
 for ap in aps:
  if ap.status:
   try:
    # make connection to device (by api)
    c = connectDevice(ap.ip, ap.login, ap.password, ap.type, logger)
    passwd = setPassword(c, hspot, ap, logger)
    ssid = setSSID(c, hspot, ap, logger)
    freq = setFreq(c, ap, logger)
    # Return 0 if OK
    return 0
   except Exception as e:
    logger.error("Unexpected error: %s" % e)
    return 1
  else:
   logger.waring("Device %s (hspot %s) is offine. Skipping..." % (ap.name, hspot.name))
   return 1

if __name__ == "__main__":
###@Need to add help()
 print "Only as a module"
 sys.exit()

