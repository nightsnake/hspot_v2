#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Category: setter, checker
# Will check settings: WiFi settings SSID, frequency, cipher
# Copyright (C) Snake, 2016 http://nixman.info
##----------------------------------------------------------------------

import os, sys, inspect
import ipaddr

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../lib")))
if cmd_subfolder not in sys.path:
 sys.path.insert(0, cmd_subfolder)
from db_devices import *
from db_devices_properties import *
from db_access_points import *
from connector import *
from config import Config
from string import Template
from base import *

def makeAPConfig(ap, project, wlan, bridge, path, hs_name, logger):
 apcfg = ''
 try:
  if ap.type == 'mkt': #check AP type
   cfg = dict(ip = ap.ip,
          gw = ap.gw.split('/')[0],
          password = ap.password,
          name = ap.name,
          project = project,
          wlan_if = wlan,
          bridge_if = bridge,
   )
   in_file = 'default_ap.rsc'
   logger.debug("[makeAPConfig] Try to open file %s in %s" % (in_file, path))
   file = open( path + in_file )
   src = Template( file.read() )
#Replace only options which defined into dict
   result = src.safe_substitute(cfg)
   out_file = ap.name + '.rsc'
   out_path = path + hs_name + '/' + out_file
   dst = open(out_path, 'w')
   dst.write(result)
   return out_file
  else:
   logger.warning("Unknown AP type %s for %s" % (ap.type, ap.name))
   return 0
 except Exception as e:
  logger.error("[makeAPConfig] Unexpected error: %s" % e)
  return -1

 return apcfg

def setExternalAP(h, hspot, ap, srv_cfg, ports, wlans, bridges, logger):
 try:
  a = access_pointsAction()
  if hspot.type == 'mkt': #check AP type
   port = ports[str(ap.port)]
   logger.debug("Preparing hspot %s for external AP in port %s" % (hspot.name, port))
   addPortToBridge(h, hspot, port, bridges['hspot'], logger)
   ip = ipaddr.IPv4Network(ap.ip)
   gw = ipaddr.IPv4Network(ap.gw)
   #Check if ip and gw placed in the same network
   if (ip == gw):
    logger.debug("Add gw address %s for AP %s on mkt" % (ap.gw, ap.name))
    addAddressToInt(h, hspot, bridges['hspot'], ap.gw, logger)
   else:
    logger.error("Netmasks for gw and address are not match. Please check settings")
    return -1
#Make bootconfig for ap
   apcfg = makeAPConfig(ap, srv_cfg['project'], wlans['hspot'], bridges['hspot'], srv_cfg['key_path'], hspot.name, logger)
   if apcfg:
    logger.debug("Startup config for %s has been written to %s" % (ap.name, apcfg))
    apurl = 'ftp://%s/%s/%s' % (srv_cfg['ftp_ip'], hspot.name, apcfg)
    logger.debug("URL for ap config: %s" % apurl)
   else:
    logger.error("[setExternalAP] Can't create bootconfig for AP")
    return -1
#   make zip with file and README
#   Make link for config file and place into DB (need to add column)
   a.setAPUrl(ap.id, apurl)
  else:
   logger.warning("Unknown AP type %s for %s" % (hspot.type, hspot.name))
   return 0
 except Exception as e:
  logger.error("[setExternalAP] Unexpected error: %s" % e)
  return -1

def setHspotWiFi(c, hspot, ap, srv_cfg, interfaces, bridges, logger):
#Set access point wireless settings
 wlans = []
 wifi_string = "/interface/wireless/print"
 profile_string = "/interface/wireless/security-profiles/print"
 try:
  if ap.type == 'mkt': #check AP type
   wlans = c.response_handler(c.talk([wifi_string]))
   profiles = c.response_handler(c.talk([profile_string]))

   default_profile = filter(lambda profile: profile['name'] == 'default', profiles)
   default_interface = filter(lambda wlan: wlan['name'] == 'wlan1', wlans)
   if default_interface and default_profile:
    logger.debug("Found interface %s and profile %s" % (default_interface[0]['name'], default_profile[0]['name']))
    s_ap = c.response_handler(c.talk(["/interface/wireless/set",
                                                               "=.id="+default_interface[0]['.id'],
                                                               "=name="+interfaces['hspot'],
                                                               "=disabled=false",
                                                               "=ssid="+hspot.ssid,
                                                               "=mode=ap-bridge",
                                                               "=wireless-protocol=802.11",
                                                               "=security-profile="+default_profile[0]['name'],
                                     ]))
#Add wireless interface to hspot bridge. Will be applied to AP
    br = addPortToBridge(c, ap, interfaces['hspot'], bridges['hspot'], logger)
    logger.debug("Hotspot WLAN was successfully added to device %s" % (ap.name))
    return 0
   else:
    logger.error("[setHspotWiFi] Unexpected error: default wlan interface or security profile not found on %s" % ap.name)
    return -1
  else:
   logger.warning("Unknown AP type %s for %s" % (ap.type, ap.name))
   return 0
 except Exception as e:
  logger.error("[setHspotWiFi] Unexpected error: %s" % e)
  return -1

def setServiceWiFi(c, hspot, ap, srv_cfg, interfaces, bridges, logger):
 service_profile = 'hs-ap-prof-service'
 profile_string = "/interface/wireless/security-profiles/print"
 wifi_string = "/interface/wireless/print"
 try:
  if ap.type == 'mkt' and ap.port == 0: #Service WiFi available only if AP placed on the hspot device
   wlans = c.response_handler(c.talk([wifi_string])) #Get list with wifi ifaces
   profiles = c.response_handler(c.talk([profile_string]))
   hs_wlan = filter(lambda hs_wlan_name: hs_wlan_name['name'] == interfaces['hspot'], wlans)
#Check security profiles
   if not filter(lambda profile: profile['name'] == service_profile, profiles):
    if (makeProfile(c, hspot, ap, logger) == -1):
     return -1
    else:
     setProfile(c, hspot, ap, logger)
   else:
    logger.debug("Security profile already exist on %s" % ap.name)
    setProfile(c, hspot, ap, logger)
#If no any service wlans
   if not filter(lambda wlan: wlan['name'] == interfaces['service'], wlans):
    s_ap = c.response_handler(c.talk(["/interface/wireless/add",
                                                                  "=name="+interfaces['service'],
                                                                  "=master-interface="+hs_wlan[0][".id"],
                                                                  "=disabled=n",
                                                                  "=ssid="+hspot.ssid,
                                                                  "=security-profile="+service_profile,
                                     ]))
    addPortToBridge(c, hspot, interfaces['service'], bridges['service'], logger)
    logger.debug("Service WLAN added to device %s" % hspot.name)
    return 1
   else:
    logger.warning("Service wlan already exist on %s" % ap.name)
    setProfile(c, hspot, ap, logger)
    return 0
  else:
   logger.warning("Unknown AP type %s for %s (or external AP detected)" % (ap.type, ap.name))
   return 0
 except Exception as e:
  logger.error("Unexpected error: %s" % e)
  return -1

def makeProfile(c, hspot, ap, logger):
 """
 Make service security profile
 """
 profile_string = "/interface/wireless/security-profiles/print"
 profile_add_string = "/interface/wireless/security-profiles/add"
 service_profile = 'hs-ap-prof-service'
 try:
  if ap.type == 'mkt':
   profiles = c.response_handler(c.talk([profile_string]))
   default_profile = filter(lambda profile: profile['name'] == 'default', profiles)
   if default_profile:
    p = c.response_handler(c.talk([profile_add_string,
                                                            "=name="+service_profile,
                                                            "copy-from="+default_profile[0]['.id']
                                        ]))
    logger.debug("Security profile created successfull on %s" % ap.name)
    return 1
   else:
    logger.error("Unexpected error: default wireless security profile not found on %s" % ap.name)
    return -1
  else:
   logger.warning("Unknown AP type %s for %s" % (ap.type, ap.name))
   return 0
 except Exception as e:
  logger.error("Unexpected error: %s" % e)
  return -1

def setProfile(c, hspot, ap, logger):
 try:
 #Set settings for Mikrotik AP
  if ap.type == 'mkt':
   profile_string = "/interface/wireless/security-profiles/print"
   profile_set_string = "/interface/wireless/security-profiles/set"
   profiles = c.response_handler(c.talk([profile_string]))
   for profile in profiles:
#Disable cipher for public hotspot network
    if 'default' in profile['name']:
     p1 = c.response_handler(c.talk([profile_set_string,
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
      p1 = c.response_handler(c.talk([profile_set_string,
                                                 "=.id="+profile['.id'],
                                                 "=wpa-pre-shared-key="+hspot.service_pass,
                                                 "=wpa2-pre-shared-key="+hspot.service_pass,
                                                 "=mode=dynamic-keys",
                                                 "=authentication-types=wpa-psk,wpa2-psk",
                                                 "=unicast-ciphers=tkip,aes-ccm",
                                                 "=group-ciphers=tkip,aes-ccm",
                                                 ]))
     else:
      p1 = c.response_handler(c.talk([profile_set_string,
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
   return 1
  else:
   logger.warning("Unknown AP type %s for %s" % (ap.type, ap.name))
   return 0
 except Exception as e:
  logger.error("[setProfile] Unexpected error: %s" % e)
  return -1

def setSSID(c, hspot, ap, srv_cfg, interface, logger):
 wlans = []
 ssid = ''
 wifi_string = "/interface/wireless/print"
 #Set settings for Mikrotik AP
 try:
  if ap.type == 'mkt':
   wlans = c.response_handler(c.talk([wifi_string]))
   for wlan in wlans:
   # Set hotspot AP, not service AP (based on default mkt adapter)
    if interface['hspot'] == wlan['name']:
     w = c.response_handler(c.talk(["/interface/wireless/set", "=.id="+wlan['.id'], "=ssid="+hspot.ssid, ]))
    #Set service_wifi AP
    elif interface['service'] == wlan['name'] and hspot.service_wifi:
     hide_ssid = hspot.service_hide and "yes" or "no"
     w = c.response_handler(c.talk(["/interface/wireless/set", "=.id="+wlan['.id'], "=ssid="+hspot.service_ssid, "=hide-ssid="+hide_ssid,]))
    else:
     logger.warning("Unknown wireless interface %s on %s" % (wlan['name'], ap.name))
   return 0
  else:
   logger.warning("Unknown AP type %s for %s" % (ap.type, ap.name))
   return 0
 except Exception as e:
  logger.error("[setSSID] Unexpected error: %s" % e)
  return -1
#return ssid

def setFreq(c, ap, srv_cfg, interface, logger):
 wifi_string = "/interface/wireless/print"
 #Set settings for Mikrotik AP
 try:
  if ap.type == 'mkt':
   wlans = c.response_handler(c.talk([wifi_string]))
   wlan = filter(lambda w: w['name'] == interface['hspot'], wlans)
   if wlan:
    w = c.response_handler(c.talk(["/interface/wireless/set", "=.id="+wlan[0]['.id'], "=frequency="+str(ap.freq), ]))
    return 0
   else:
    logger.error("HotSpot AP not found on %s" % (ap.name))
    return -1
  else:
   logger.warning("Unknown AP type %s for %s" % (ap.type, ap.name))
   return 0
 except Exception as e:
  logger.error("[setFreq] Unexpected error: %s" % e)
  return -1

#return freq

def setWiFi(ap, logger):
 # Check not hspots, but access points
 a = devAction()
 t = devices_propertiesAction()
 p = access_pointsAction()
 wlans = {}
 bridges = {}
 ports = {}
 #Load vars from config
 try:
  config = Config()
  srv_cfg = config.getServerConfig()
  logger.debug("Load settings from config")
  wlans, bridges, ports = config.getWlanConfig(logger)
  logger.debug("loaded: ports %s bridges %s wlans %s" % (ports['0'], bridges['hspot'], wlans['hspot']))
 except Exception as e:
  logger.error("[setWiFi] Can't load config: %s" % e)
  return -1

 hs_id = p.getHspotIdByAP(ap.id)
 hspot = a.devGetById(hs_id)

 aps = [ap]

 for ap in aps:
  if (ap.status) and (hspot.status) and (ap.done != 1):
   try:
    # make connection to device (by api)
    c = connectDevice(ap.ip, ap.login, ap.password, ap.type, logger)
    h = connectDevice(hspot.ip, hspot.login, hspot.password, hspot.type, logger)

    logger.debug("AP %s in port %s" % (ap.name, ap.port))
    if ap.port > 0:
     ext_ap = setExternalAP(h, hspot, ap, srv_cfg, ports, wlans, bridges, logger)
    if c != -1:
     hs_wifi = setHspotWiFi(c, hspot, ap, srv_cfg, wlans, bridges, logger)
     service = setServiceWiFi(c, hspot, ap, srv_cfg, wlans, bridges, logger)

     passwd = setProfile(c, hspot, ap, logger)
     ssid = setSSID(c, hspot, ap, srv_cfg, wlans, logger)
     freq = setFreq(c, ap, srv_cfg, wlans, logger)
    else:
     logger.error("[setWiFi] Can't connect to device: %s" % ap.name)
     return 0
    # Return 0 if OK
    return 1
   except Exception as e:
    logger.error("[setWiFi] unexpected error: %s" % e)
    return -1
  else:
   #If hotspot is offline (or hspot + internal AP)
   if not (hspot.status):
    logger.warning("[setWiFi] hspot %s is offline. Skipping..." % (hspot.name))
    return 0
   #If external AP and it's not configured
   elif (ap.port > 0) and (ap.done != 1):
    ext_ap = setExternalAP(h, hspot, ap, srv_cfg, ports, wlans, bridges, logger)
    return 1
   #If AP is done
   else:
    logger.warning("[setWiFi] Device %s (hspot %s) is already configured. Skipping..." % (ap.name, hspot.name))
    return 0

if __name__ == "__main__":
###@Need to add help()
 print "Only as a module"
 sys.exit()

