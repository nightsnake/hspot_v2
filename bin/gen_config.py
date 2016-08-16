#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Config generator
# Make a config for Mikrotik HotSpot
# Copyright 2016 (c) Snake, <snake@nixman.info> @night_snake
##----------------------------------------------------------------------

import os, sys, inspect, getopt
import subprocess
import ipaddr

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../lib")))
if cmd_subfolder not in sys.path:
 sys.path.insert(0, cmd_subfolder)

from logger import *
from string import Template
from config import Config
from db_devices import *
from base import *
from gen_ovpn import ovpn_generator


def getHspotSettings(srv_cfg, spot):
    cfg = {}

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
    ftp_url = "ftp://" + ftp_ip
    http_url = "http://cp." + site
    wifi_url = "wifi." + site

    network = ipaddr.IPv4Network(spot.network)
    hsgw = network[1]
    hsranbgn = network[2]
    hsranend = network[-2]
    gw = spot.gw
    ssid = spot.ssid
    radius = spot.server
    secret = spot.secret
    name = spot.name
    password = spot.password
    s_enable = spot.service_wifi and "yes" or "no"
    s_ssid = spot.service_ssid
    s_hide = spot.service_hide and "yes" or "no"
    s_enc = spot.service_encryption
    s_pass = spot.service_pass
    cfg = {'srv':server_ip, 
           'project':project, 
           'hsgw':hsgw, 
           'hsranbgn':hsranbgn, 
           'hsranend':hsranend, 
           'network':network, 
           'gw':gw,
           'password':password, 
           'ssid':ssid, 
           'name':name, 
           'radius':radius, 
           'url':ftp_url, 
           'ftp_user':ftp_user, 
           'ftp_password':ftp_password,
           'service_wifi':s_enable,
           'service_ssid':s_ssid, 
           'service_hide':s_hide, 
           'service_encryption':s_enc, 
           'service_pass':s_pass, 
           'wifi_url':wifi_url
           }
    
    return key_path, http_url, cfg

def setConfigFiles(spot, skel_files, cfg, skel_full_path, key_path, name, logger):
####
    dst = ''    
    for f in skel_files:
     filein = open( skel_full_path + f )
     src = Template( filein.read() )
     logger.debug("Skel file is %s..." % f)
#### Create dir for files
     try:
      out_path = mkdir(key_path + name, logger) + '/' + f
      logger.debug("Set output path as %s..." % out_path)
#### Try to create config in directory
      try:
       dst = open(out_path, 'w')
       try:
        result = src.substitute(cfg)
        dst.write(result)
       except Exception as e:
        logger.warning("Failed to generate config for %s in %s: %s" %(f, spot.name, e))
       dst.close()
      except:
       logger.warning("Failed to create config file: %s in %s" % (f, spot.name))
       continue
     except:
      logger.warning("Failed to create directory: %s" % spot.name)

def genFetcher (files, name, ftp_url, user, password, fetch_path, in_path, logger):
    """
    Prepare fetcher, which download all other configs
    """

    dst = ''
    in_file = "fetcher.cfg"
    tar_file = "fetcher.tar.gz"
    rsc_file = "default.rsc"
    in_file_path = in_path + in_file

    out_file = name + "/" + in_file
    out_file_path = fetch_path + out_file
    tar_file_path = fetch_path + tar_file
    rsc_file_path = fetch_path + rsc_file

    retval = os.getcwd()

    filein = open( in_file_path )
    try:
     src = Template( filein.read() )
     dst = open(out_file_path, 'w')
     for f in files:
      cfg = {'name':name, 'file':f, 'url':ftp_url, 'ftp_user':user, 'ftp_password':password}
      result = src.substitute(cfg)
      dst.write(result)
     dst.close()
#### Make archive with fetcher and mkt default config
     os.chdir( fetch_path )
     build_tar(tar_file, [out_file_path, rsc_file_path])
    except Exception as e:
     logger.warning("Failed to generate fetching list: %s" % e)

def makeConfig(id, logger):
    """
    Config generator for Mikrotik
    """
#Describe paths
    skel_path = "../etc/skel/"
    etc_path = "../etc/"
    srv_cfg_path = etc_path + "server.cfg"
    base_dir = os.getcwd()
    skel_full_path = os.path.join(base_dir, skel_path)
    etc_full_path = os.path.join(base_dir, etc_path)
    abs_file_path = os.path.join(base_dir, srv_cfg_path)

#Load vars from config    
    config = Config()
    srv_cfg = config.getServerConfig()

#Load skel files
    skel_files = filelist(skel_full_path)
#Load hotspot by ID
    a = devAction()
    spot = a.devGetById(id)
    if not spot:
      logger.warning("Failed to create config: hspot id not found")
      sys.exit(1)

    logger.debug("Prepare settings...")
    key_path, http_url, cfg = getHspotSettings(srv_cfg, spot)
    logger.debug("Making config files...")      
    setConfigFiles(spot, skel_files, cfg, skel_full_path, key_path, spot.name, logger)

#### Marking device as 'new'
    a.devSetNew(spot.id)
#### Make fetcher.cfg
    logger.debug("Making fetcher file...")
    genFetcher(skel_files, spot.name, cfg['url'], cfg['ftp_user'], cfg['ftp_password'], key_path, etc_full_path, logger)
#### Make openvpn files
    logger.debug("Making openvpn files...")
    ovpn_generator(spot.name, 'client', 'client', '10.0.0.1', spot.ip, logger)
#### Create link for customer
    try:
      cfg_url = http_url + "/cfg/" + spot.name + ".zip"
      a.devSetConfigURL(id, cfg_url)
    except:
      logger.warning("Failed to moving config for %s" % spot.name)

if __name__ == "__main__":
    if len(sys.argv) > 1:
     try:
      id = sys.argv[1]
      logger = logger("hs-generator")
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
