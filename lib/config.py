#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Category: base functions
# Will get configuration from file
# Copyright (C) Snake, 2016
##----------------------------------------------------------------------

import os, sys, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../lib")))
if cmd_subfolder not in sys.path:
 sys.path.insert(0, cmd_subfolder)
#from logger import *

class Config():
 import ConfigParser
 base_dir = os.path.dirname(__file__)
 etc_path = "../etc/"
 srv_cfg_path = etc_path + "server.cfg"
 abs_file_path = os.path.join(base_dir, srv_cfg_path)
 config = ConfigParser.ConfigParser()
 config.read(abs_file_path)

 def getServerConfig(self):
    #### Load from config file
    srv_cfg = {}
    srv_cfg['project']  = self.config.get('server', 'project')
    srv_cfg['server_ip'] = self.config.get('server', 'server_ip')
    srv_cfg['ovpn_ip'] = self.config.get('server', 'ovpn_ip')
    srv_cfg['ftp_ip'] = self.config.get('server', 'ftp_ip')
    srv_cfg['ftp_user'] = self.config.get('server', 'ftp_user')
    srv_cfg['ftp_password'] = self.config.get('server', 'ftp_password')
    srv_cfg['site'] = self.config.get('server', 'site')
    srv_cfg['key_path'] = self.config.get('server', 'key_path')
    srv_cfg['hspot_path'] = self.config.get('server', 'hspot_path')
    srv_cfg['cfg_path'] = self.config.get('server', 'cfg_path')
    #### end of loading from file
    return srv_cfg

 def getCertConfig(self):
    cert_cfg = {}
    cert_cfg['stateOrProvinceName'] = self.config.get('certificate', 'stateOrProvinceName')
    cert_cfg['localityName'] = self.config.get('certificate', 'localityName')
    cert_cfg['organizationName'] = self.config.get('certificate', 'organizationName')
    cert_cfg['organizationalUnitName'] = self.config.get('certificate', 'organizationalUnitName')
    cert_cfg['emailAddress'] = self.config.get('certificate', 'emailAddress')
    cert_cfg['countryName'] = self.config.get('certificate', 'countryName')
    cert_cfg['validfrom'] = self.config.get('certificate', 'validfrom')
    cert_cfg['validto'] = self.config.get('certificate', 'validto')
    cert_cfg['keyfilesize'] = self.config.get('certificate', 'keyfilesize')
    cert_cfg['hashalgorithm'] = self.config.get('certificate', 'hashalgorithm')
    return cert_cfg

 def getLogConfig(self):
    log_cfg = {}
    log_cfg['level'] = self.config.get('log', 'log_level')
    log_cfg['path'] = self.config.get('log', 'log_path')  
    return log_cfg

 def getWlanConfig(self, logger):
  ports = {}
  bridges = {}
  wlans = {}
  try:
    ports['0'] = self.config.get('interfaces', 'port0')
    ports['1'] = self.config.get('interfaces', 'port1')
    ports['2'] = self.config.get('interfaces', 'port2')
    ports['3'] = self.config.get('interfaces', 'port3')
    ports['4'] = self.config.get('interfaces', 'port4')
    ports['5'] = self.config.get('interfaces', 'port5')
    bridges['hspot'] = self.config.get('interfaces', 'hs_bridge')
    bridges['service'] = self.config.get('interfaces', 'sr_bridge')
    wlans['hspot'] = self.config.get('interfaces', 'hs_ap')
    wlans['service'] = self.config.get('interfaces', 'sr_ap')
  except Exception as e:
    logger.warning("[Config] Can't load settings from config: %s" % e)
  else:
    return (wlans, bridges, ports)

 def getOVPNConfig(self):
  ovpn_cfg = {}
  ovpn_cfg['DH_PARAM_SIZE'] = self.config.get('openvpn','DH_PARAM_SIZE')
  ovpn_cfg['ovpn_path'] = self.config.get('openvpn','ovpn_path')
  ovpn_cfg['ovpn_srv'] = self.config.get('openvpn','ovpn_srv')
  ovpn_cfg['key_outpath'] = self.config.get('openvpn','key_outpath')

  return ovpn_cfg
  
if __name__ == "__main__":
    print "Only module format allowed"
#    print "Project: "+Config.project
#    print "Server: "+Config.server_ip
#    print "OVPN: "+Config.ovpn_ip    
#    print "FTP: "+Config.ftp_ip
#    print "FTP: "+Config.ftp_user
#    print "FTP: "+Config.ftp_password
#    print "Site: "+Config.site
    sys.exit()
