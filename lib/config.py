#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# get config from file
# Copyright (C) Snake, 2015
##----------------------------------------------------------------------

import os, sys, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../lib")))
if cmd_subfolder not in sys.path:
 sys.path.insert(0, cmd_subfolder)
from logger import *

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
    project  = self.config.get('server', 'project')
    server_ip = self.config.get('server', 'server_ip')
    ovpn_ip = self.config.get('server', 'ovpn_ip')
    ftp_ip = self.config.get('server', 'ftp_ip')
    ftp_user = self.config.get('server', 'ftp_user')
    ftp_password = self.config.get('server', 'ftp_password')
    site = self.config.get('server', 'site')
    key_path = self.config.get('server', 'key_path')
    hspot_path = self.config.get('server', 'hspot_path')
    cfg_path = self.config.get('server', 'cfg_path')
    #### end of loading from file
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
      
if __name__ == "__main__":
    print "Only module format allowed"
    print "Project: "+Config.project
    print "Server: "+Config.server_ip
    print "OVPN: "+Config.ovpn_ip    
    print "FTP: "+Config.ftp_ip
    print "FTP: "+Config.ftp_user
    print "FTP: "+Config.ftp_password
    print "Site: "+Config.site
    sys.exit()
