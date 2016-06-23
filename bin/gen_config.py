#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Config generator
# Make a config for Mikrotik HotSpot
# Copyright 2016 (c) Snake, <snake@nixman.info> @night_snake
##----------------------------------------------------------------------

import os, sys, inspect, getopt
import subprocess

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../lib")))
if cmd_subfolder not in sys.path:
 sys.path.insert(0, cmd_subfolder)

from logger import *
from config import Config
from devices import *
from base import *
from ovpn import *

def makeConfig(id, logger):
    """
    Config generator for Mikrotik
    """
#Describe paths
    skel_path = "../etc/skel/"
    etc_path = "../etc/"
    srv_cfg_path = etc_path + "server.cfg"
    base_dir = = os.getcwd()

    skel_full_path = os.path.join(base_dir, skel_path)
    etc_full_path = os.path.join(base_dir, etc_path)
    abs_file_path = os.path.join(base_dir, srv_cfg_path)

    config = Config()
    srv_cfg = config.getServerConfig()
    
    project = srv_cfg['project']
    server_ip = srv_cfg['server_ip']
    ovpn_ip = srv_cfg['ovpn_ip']
    ftp_ip = srv_cfg['ftp_ip']
    ftp_user = srv_cfg['ftp_user']
    ftp_password = srv_cfg['ftp_password']
    site = srv_cfg['site']
    key_path = srv_cfg['key_path']
    hspot_path = srv_cfg['hspot_path']
    cfg_path = srv_cfg['cfg_path']

    a = devAction()
    
    ftp_url = "ftp://" + ftp_ip
    http_url = "http://cp." + site
    wifi_url = "wifi." + site

    skel_files = filelist(skel_full_path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
     try:
      id = sys.argv[1]
      logger = logger("config", 10)
      logger.debug("Hotspot ID: " + id)
      makeConfig(id, logger)
     except Exception as e:
      logger.warning("Unexpected error: " + sys.argv[0] + " [id]")
	  sys.stderr.write("Error: %s\n" % e)
	  sys.exit(1)
	 else:	  
	  sys.exit(0)
    else:
	 sys.stdout.write("You have to define device id: %s <id>\n" % sys.argv[0])
     sys.exit(1)
