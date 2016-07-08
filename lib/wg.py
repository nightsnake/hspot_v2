#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# module for checking WG settings
# Copyright 2016 (c) Snake, <snake@nixman.info> @night_snake
##----------------------------------------------------------------------

import os, sys, inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../lib")))
if cmd_subfolder not in sys.path:
 sys.path.insert(0, cmd_subfolder)

from db_devices_properties import *
from connector import *

def getCNASettings(c, logger):
 #Get id's of WG strings
 try:
  wg_string = '/ip/hotspot/walled-garden/print'
  cna_apple = c.response_handler(c.talk([wg_string, "?comment="+"apple"]))
  cna_android = c.response_handler(c.talk([wg_string, "?comment="+"android"]))
  cna_win = c.response_handler(c.talk([wg_string, "?comment="+"win"]))
  return cna_apple, cna_android, cna_win
 except Exception as e:
  logger.error("Unexpected error: %s" % e)
 else: 
  return 0

def setCNASettings(cna_apple, cna_android, cna_win, wg, c):
 try:
  #Get CNA status from DB
  cna_apple_disable = wg.captive_apple and "yes" or "no"
  cna_android_disable = wg.captive_android and "yes" or "no"
  cna_win_disable = wg.captive_win and "yes" or "no"
 
  #Set settings to device
  wg_set_string = "/ip/hotspot/walled-garden/set"
  for cna_entry in cna_apple:
   c.response_handler(c.talk([wg_set_string, "=.id="+cna_entry['.id'], "=disabled="+cna_apple_disable]))
  for cna_entry in cna_android:
   c.response_handler(c.talk([wg_set_string, "=.id="+cna_entry['.id'], "=disabled="+cna_android_disable]))
  for cna_entry in cna_win:
   c.response_handler(c.talk([wg_set_string, "=.id="+cna_entry['.id'], "=disabled="+cna_win_disable]))
  return 1
 except Exception as e:
  logger.error("Unexpected error: %s" % e)
 else:
  return 0

def getSocialSettings(c, social, logger):

 wg_social = []
 social_list = ['vk', 'fb', 'tw', 'ok', 'in']
 social_status = {'vk':'yes', 'fb':'yes', 'tw':'yes', 'ok':'yes', 'in':'yes'}
 try:
  for s in list(social):
 # Say 'no' if you want to allow social login (disabled=no)
 # Say 'yes' if you want to block social login (disabled=yes)
   social_status[social_list[int(s)-1]] = 'no'

  wg_string = "/ip/hotspot/walled-garden/print"
  wg_ip_string = "/ip/hotspot/walled-garden/ip/print"
  #Get settings from device
  wg_social['vk'] = c.response_handler(c.talk([wg_string, "?comment="+"vk"]))
  wg_social['vk_ip'] = c.response_handler(c.talk([wg_ip_string, "?comment="+"vk"]))
  wg_social['ok'] = c.response_handler(c.talk([wg_string, "?comment="+"ok"]))
  wg_social['ok_ip'] = c.response_handler(c.talk([wg_ip_string, "?comment="+"ok"]))
  wg_social['fb'] = c.response_handler(c.talk([wg_string, "?comment="+"fb"]))
  wg_social['fb_ip'] = c.response_handler(c.talk([wg_ip_string, "?comment="+"fb"]))
  wg_social['tw'] = c.response_handler(c.talk([wg_string, "?comment="+"tw"]))
  wg_social['tw_ip'] = c.response_handler(c.talk([wg_ip_string, "?comment="+"tw"]))
  wg_social['in'] = c.response_handler(c.talk([wg_string, "?comment="+"insta"]))
  wg_social['in_ip'] = c.response_handler(c.talk([wg_ip_string, "?comment="+"in"]))
 
  return wg_social, social_status
 except Exception as e:
  logger.error("Unexpected error: %s" % e)
 else:
  return 0


def setSocialSettings(wg, wg_social, social_status, c, logger):
 try:
  wg_set_string = "/ip/hotspot/walled-garden/ip/set"
  wg_ip_set_string = "/ip/hotspot/walled-garden/set"
  #Set settings to device
  #Need to optimize strings: "for" cycle in request
  for vk_ip_entry in wg_ip_vk:
   c.response_handler(c.talk([wg_set_string, "=.id="+vk_ip_entry['.id'], "=disabled="+social_status['vk']]))
  for fb_ip_entry in wg_ip_fb:
   c.response_handler(c.talk([wg_set_string, "=.id="+fb_ip_entry['.id'], "=disabled="+social_status['fb']]))
  for tw_ip_entry in wg_ip_tw:
   c.response_handler(c.talk([wg_set_string, "=.id="+tw_ip_entry['.id'], "=disabled="+social_status['tw']]))
  for ok_ip_entry in wg_ip_ok:
   c.response_handler(c.talk([wg_set_string, "=.id="+ok_ip_entry['.id'], "=disabled="+social_status['ok']]))
  for in_ip_entry in wg_ip_in:
   c.response_handler(c.talk([wg_set_string, "=.id="+in_ip_entry['.id'], "=disabled="+social_status['in']]))

  for vk_entry in wg_vk:
   c.response_handler(c.talk([wg_ip_set_string, "=.id="+vk_entry['.id'], "=disabled="+social_status['vk']]))
  for fb_entry in wg_fb:
   c.response_handler(c.talk([wg_ip_set_string, "=.id="+fb_entry['.id'], "=disabled="+social_status['fb']]))
  for tw_entry in wg_tw:
   c.response_handler(c.talk([wg_ip_set_string, "=.id="+tw_entry['.id'], "=disabled="+social_status['tw']]))
  for ok_entry in wg_ok:
   c.response_handler(c.talk([wg_ip_set_string, "=.id="+ok_entry['.id'], "=disabled="+social_status['ok']]))
  for in_entry in wg_in:
   c.response_handler(c.talk([wg_ip_set_string, "=.id="+in_entry['.id'], "=disabled="+social_status['in']]))
 
  return 1
 except Exception as e:
  logger.error("Unexpected error: %s" % e)
 else:
  return 0

def setWG(hspot, logger):
 t = devices_propertiesAction()
 wg_social = []
 if hspot.status:
  try:
   # make connection to device (by api)
   c = connectDevice(hspot.ip, hspot.login, hspot.password, hspot.type, logger)

   # Load settings from DB
   wg = t.getSettingsById(hspot.id)

   # get status from device
   ###@ Need to load CNA settings from DB
   cna_apple, cna_android, cna_win = getCNASettings(c, logger)
   # Write settings to device
   ###@ Need to add DD-WRT support
   # Must return 1 if success
   setCNASettings(cna_apple, cna_android, cna_win, wg, c)
   ###@ Need to load social settings from DB
   wg_social, social_status = getSocialSettings(c, wg.social, logger)   
   # Write to device 
   # Must return 1 if success
   setSocialSettings(wg, wg_social, social_status, c, logger)
   # Return 0 if OK
   return 0
  except Exception as e:
   logger.error("Unexpected error: %s" % e)
   return 1
 else:
  logger.waring("Device %s is offine. Skipping..." % hspot.name)
  return 1

if __name__ == "__main__":
###@Need to add help()
 print "Only as a module"
 sys.exit()

