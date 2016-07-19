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
from config import Config


def setHspotWiFi(c, hspot, ap, srv_cfg, logger):
#Set hspot wifi interface
 wlans = []
 wifi_string = "/interface/wireless/print"
 profile_string = "/interface/wireless/security-profiles/print"
 hs_ap_name = 'hs-ap-'+srv_cfg['project']
 hs_br_name = 'hs-br-'+srv_cfg['project']
 try:
  if ap.type eq 'mkt':
   wlans = c.response_handler(c.talk([wifi_string]))
   profiles = c.response_handler(c.talk([profile_string]))

   default_profile = filter(lambda profile: profile['name'] == 'default', profiles)
   default_interface = filter(lambda wlan: wlan['name'] == 'wlan1', wlans)   
   if default_interface and default_profile:
    s_ap = c.response_handler(c.talk(["/interface/wireless/set",
                                                               "=id="+default_interface[0]['.id']
                                                               "=name="+hs_ap_name,
                                                               "=disabled=n",
                                                               "=ssid="+hspot.ssid,
                                                               "=security-profile="+default_profile[0]['name'],
                                     ]))
    s_br = c.response_handler(c.talk([""/interface/bridge/port/add",
                                                                  "=interface="+hs_ap_name,
                                                                  "=bridge="+hs_br_name,
                                     ]))
    logger.debug("Hotspot WLAN successfully added to device %s" % (ap.name))
    return 0
   else:
    logger.error("Unexpected error: default wlan interface or security profile not found on %s" % ap.name)
    return 1    
  else:
   logger.warning("Unknown AP type %s for %s" % (ap.type, ap.name))
   return 0
 except Exception as e:
  logger.error("Unexpected error: %s" % e)
  return 1
 
def setServiceWiFi(c, hspot, ap, srv_cfg, logger):
 hs_ap_name = 'hs-ap-'+srv_cfg['project']
 hs_br_name = 'hs-bridge'
 service_wifi = 'hs-ap-service'
 service_profile = 'hs-ap-prof-service'
 profile_string = "/interface/wireless/security-profiles/print"
 wifi_string = "/interface/wireless/print"
 try:
  if ap.type eq 'mkt':
   wlans = c.response_handler(c.talk([wifi_string])) #Get list with wifi ifaces
   profiles = c.response_handler(c.talk([profile_string]))
   hs_wlan = filter(lambda hs_wlan_name: hs_wlan_name['name'] == hs_ap_name, wlans)   
#Check security profiles
   if not filter(lambda profile: profile['name'] == service_profile, profiles):
    if makeProfile(c, hspot, ap, logger):
     return 1
    else:
     setProfile(c, hspot, ap, logger)
   else:
    logger.debug("Security profile already exist on %s" % ap.name)
    setProfile(c, hspot, ap, logger)
#If no any service wlans   
   if not filter(lambda wlan: wlan['name'] == service_wifi, wlans):
    s_ap = c.response_handler(c.talk(["/interface/wireless/add", 
                                                                  "=name="+service_wifi,
                                                                  "=master-interface="+hs_wlan[0][".id"], 
                                                                  "=disabled=n", 
                                                                  "=ssid="+hspot.ssid, 
                                                                  "=security-profile="+service_profile,
                                     ]))    
    s_br = c.response_handler(c.talk([""/interface/bridge/port/add",
                                                                  "=interface="+service_wifi,
                                                                  "=bridge="+hs_br_name,
                                         ]))
    logger.debug("Service WLAN added to device %s" % hspot.name)
    return 0    
   else:
    logger.warning("Service wlan already exist on %s" % ap.name)
    setProfile(c, hspot, ap, logger)
    return 0
  else:
   logger.warning("Unknown AP type %s for %s" % (ap.type, ap.name))
   return 0
 except Exception as e:
  logger.error("Unexpected error: %s" % e)
  return 1

def makeProfile(c, hspot, ap, logger):
 """
 Make service security profile
 """
 profile_string = "/interface/wireless/security-profiles/print"
 profile_add_string = "/interface/wireless/security-profiles/add"
 service_profile = 'hs-ap-prof-service'
 try:
  if ap.type eq 'mkt':
   profiles = c.response_handler(connect.talk([profile_string]))
   if default_profile = filter(lambda profile: profile['name'] == 'default', profiles):
    p = c.response_handler(connect.talk([profile_add_string,
                                                            "=name="+service_profile,
                                                            "copy-from="+default_profile[0]['.id']
                                        ]))
    logger.debug("Security profile created successfull on %s" % ap.name)
    return 0
   else:
    logger.error("Unexpected error: default wireless security profile not found on %s" % ap.name)
    return 1
  else:
   logger.warning("Unknown AP type %s for %s" % (ap.type, ap.name))
   return 0
 except Exception as e:
  logger.error("Unexpected error: %s" % e)
  return 1

def setProfile(c, hspot, ap, logger):
 try:
 #Set settings for Mikrotik AP
  if ap.type eq 'mkt':
   profile_string = "/interface/wireless/security-profiles/print"
   profile_set_string = "/interface/wireless/security-profiles/set"
   profiles = c.response_handler(connect.talk([profile_string]))
   for profile in profiles:
#Disable cipher for public hotspot network
    if 'default' in profile['name']:
     p1 = c.response_handler(connect.talk([profile_set_string, 
                                                "=.id="+profile['.id'],
                                                "=mode=none",
                                                "=authentication-types=",
                                                "=unicast-ciphers=",
                                                "=group-ciphers=",
                                                "=wpa-pre-shared-key=",
                                                "=wpa2-pre-shared-key=",
                                                ]))
    elif 'hs-ap-prof-service' in profile['name']:
     if hspot.service_encryption and hspot.service_wifi:      
      p1 = c.response_handler(connect.talk([profile_set_string, 
                                                 "=.id="+profile['.id'], 
                                                 "=wpa-pre-shared-key="+hspot.service_pass, 
                                                 "=wpa2-pre-shared-key="+hspot.service_pass,
                                                 "=mode=dynamic-keys", 
                                                 "=authentication-types=wpa-psk,wpa2-psk",
                                                 "=unicast-ciphers=tkip,aes-ccm", 
                                                 "=group-ciphers=tkip,aes-ccm",
                                                 ]))
     else:
      p1 = c.response_handler(connect.talk([profile_set_string, 
                                                 "=.id="+profile['.id'],
                                                 "=mode=none",
                                                 "=authentication-types=",
                                                 "=unicast-ciphers=",
                                                 "=group-ciphers=",
                                                 "=wpa-pre-shared-key=",
                                                 "=wpa2-pre-shared-key=",    
                                                 ]))
    else:
     logger.warning("Unknown wireless security profile %s on %s" % (profile['name'], ap.name)) 
   return 0
  else:
   logger.warning("Unknown AP type %s for %s" % (ap.type, ap.name))
   return 0
 except Exception as e:
  logger.error("Unexpected error: %s" % e)
  return 1

def setSSID(c, hspot, ap, srv_cfg, logger):
 wlans = []
 ssid = ''
 wifi_string = "/interface/wireless/print"
 service_wifi = 'hs-ap-service'
 hs_ap_name = 'hs-ap-'+srv_cfg['project']
 #Set settings for Mikrotik AP
 try:
  if ap.type eq 'mkt':
   wlans = c.response_handler(c.talk([wifi_string]))
   for wlan in wlans:
   # Set hotspot AP, not service AP (based on default mkt adapter)
    if hs_ap_name == wlan['name']:
     w = c.response_handler(c.talk(["/interface/wireless/set", "=.id="+wlan['.id'], "=ssid="+hspot.ssid, ]))
    #Set service_wifi AP
    elif service_wifi == wlan['name'] and hspot.service_wifi:
     hide-ssid = hspot.service_hide and "yes" or "no"      
     w = c.response_handler(c.talk(["/interface/wireless/set", "=.id="+wlan['.id'], "=ssid="+hspot.service_ssid, "=hide-ssid="+hide-ssid,]))
    else:
     logger.warning("Unknown wireless interface %s on %s" % (wlan['name'], ap.name))
   return 0
  else:
   logger.warning("Unknown AP type %s for %s" % (ap.type, ap.name))
   return 0
 except Exception as e:
  logger.error("Unexpected error: %s" % e)
  return 1
#return ssid

def setFreq(c, ap, srv_cfg, hspot):
 wifi_string = "/interface/wireless/print"
 hs_ap_name = 'hs-ap-'+srv_cfg['project']
 #Set settings for Mikrotik AP
 try:
  if ap.type eq 'mkt':
   wlans = c.response_handler(c.talk([wifi_string]))
   if wlan = filter(lambda w: w['name'] == hs_ap_name, wlans)   
    w = c.response_handler(c.talk(["/interface/wireless/set", "=.id="+wlan[0]['.id'], "=frequency="+ap.freq, ]))
    return 0
   else:
    logger.error("HotSpot AP not found on %s" % (ap.name))
    return 1
  else:
   logger.warning("Unknown AP type %s for %s" % (ap.type, ap.name))
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
 #Load vars from config
 config = Config()
 srv_cfg = config.getServerConfig()

 aps = p.getAPByHspotId(hspot.id)
 for ap in aps:
  if ap.status:
   try:
    # make connection to device (by api)
    c = connectDevice(ap.ip, ap.login, ap.password, ap.type, logger)
    hs_wifi = setHspotWiFi(c, hspot, ap, srv_cfg, logger)
    service = setServiceWiFi(c, hspot, ap, srv_cfg, logger)

    passwd = setProfile(c, hspot, ap, srv_cfg, logger)
    ssid = setSSID(c, hspot, ap, srv_cfg, logger)
    freq = setFreq(c, ap, srv_cfg, logger)
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

