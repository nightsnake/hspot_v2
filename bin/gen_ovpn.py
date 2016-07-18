#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# OpenVPN Generator
# This will make a config and keys for OpenVPN
# Copyright 2016 (c) Snake, <snake@nixman.info> @night_snake
##----------------------------------------------------------------------



import os, sys, inspect, getopt
import subprocess

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../lib")))
if cmd_subfolder not in sys.path:
 sys.path.insert(0, cmd_subfolder)

from logger import *
from config import Config
from base import *
from ovpn import *
from OpenSSL import crypto


DH_PARAM_SIZE = 4096
###@Need to move to cfg
ovpn_path = '/home/snake/hotspot2/etc/openvpn'
ovpn_srv = '10.0.0.1'

def instructions():
    """
    Show short instructions about certificates
    """    

    sys.stdout.write(colourise("On the OpenVPN Server:\n",'0;40'))
    sys.stdout.write(colourise("ca ca.pem\n",'0;32'))
    sys.stdout.write(colourise("cert server.pem\n",'0;32'))
    sys.stdout.write(colourise("key server.key\n",'0;32'))
    sys.stdout.write("\n")
    sys.stdout.write(colourise("On the OpenVPN Client:\n",'0;40'))
    sys.stdout.write(colourise("ca ca.pem\n",'0;32'))
    sys.stdout.write(colourise("cert client.pem\n",'0;32'))
    sys.stdout.write(colourise("key client.key\n",'0;32'))
    sys.stdout.write("\n")

def ovpn_generator(certname, certype, cfgtype, srv_ip, cli_ip):
    """
    function for external calls (unattended)
    """
    client_key_path = ovpn_path + '/easy-rsa/keys/'
    retval = os.getcwd()

    if (certype == 'server' or certype == 'client') and certname:
     os.chdir( ovpn_path )
     # Now build ta.key and dh params if they do not already exist
     build_openssl_extra()
     # Make a certconfig
     cert_cfg = certcfg(certname, certype)
     # Make keys (CA, Server or Client)
     ca_cert, ca_key, cert_cert, cert_key = gen_cert(cert_cfg, certype, certname, ovpn_path)
     # Make static ip for client, if defined
     if certype == 'client' and cli_ip:
      os.chdir( ovpn_path )
      gen_staticlients(certname, cli_ip, ovpn_srv)
    elif certype:
      ###@ Need to add logg.error (unknown cert type or undefined certname)
      return 0      
     
    # Make configs for client and server
    if cfgtype == 'server':
     os.chdir( ovpn_path )
     gen_server_config(DH_PARAM_SIZE)
    elif cfgtype == 'client' and srv_ip:
     os.chdir( retval + '/../tmp')
     gen_client_config(certname, srv_ip)
     os.chdir( retval )
    elif cfgtype:
    ###@ Need to replace to logg.error
#     print "Unknown config type: %s or ovpn srv IP is not defined. Exiting..." % cfgtype
     return 0

    return 1

def help():
#Help for standalone usage
    pass

def main(argv):
    """
    Main call. Interactive output
    """
    cert_cfg = {}
    certname = ''
    certype = ''
    cfgtype = ''
    cli_ip = ''
    srv_ip = ''
#    ovpn_srv = '10.0.0.1'
#    ovpn_path = '/home/snake/hotspot2/etc/openvpn'
    client_key_path = ovpn_path + '/easy-rsa/keys/'
    retval = os.getcwd()

    try:
###@If verbose defined, show logs on screen
      opts, args = getopt.getopt(argv,"hvn:k:c:a:s:",["name=","keytype=","cfgtype=", "address=", "server=", "verbose", "help"])
    except getopt.GetoptError:
      print 'Unkown option'
###@ Need to add help() with information about keys and options
      print 'gen_ovpn.py -n <cert_name>|--name=<cert_name> [--keyca] --keytype=server|client|ca --cfgtype=server|client --address=10.0.1.1]'
      sys.exit(2)
    except Exception as e:
        sys.stdout.write("Error: %s\n" % e)
        sys.exit(1)
    for opt, arg in opts:
      if opt == '-h':
###@ Need to add help() with information about keys and options
         print 'gen_ovpn.py -n <cert_name>|--name=<cert_name> [--keytype=server|client|ca --cfgtype=server|client]'
         sys.exit()
      elif opt == '-n' or opt == '--name':
         certname = arg
      elif opt == '-k' or opt == '--keytype':
         certype = arg
      elif opt == '-c' or opt == '--cfgtype':
         cfgtype = arg
      elif opt == '-a' or opt == '--address':
         cli_ip = arg
      elif opt == '-s' or opt == '--server':
         srv_ip = arg
      else:
###@ Need to replace to logg.error
#         print "Unknown option: %s" % opt
         sys.exit(1)
    if certype:
     # Make a certconfig
     cert_cfg = certcfg(certname, certype)
 
     # Get keys (CA, Server or Client)
     ca_cert, ca_key, cert_cert, cert_key = gen_cert(cert_cfg, certype, certname, ovpn_path)
     # Now build ta.key and dh params if they do not already exist
     os.chdir( ovpn_path )
     if certype == 'client' and cli_ip:
      gen_staticlients(certname, cli_ip, ovpn_srv)
      build_openssl_extra()
      sys.stdout.write("\n")
      # Get some manual to user
      instructions()
    # Make configs for client and server
    if cfgtype == 'server':
     os.chdir( ovpn_path )
     gen_server_config(DH_PARAM_SIZE)
    elif cfgtype == 'client' and srv_ip:
     tmp_dir = retval + '/../tmp'
     os.chdir( tmp_dir )
     gen_client_config(certname, srv_ip)          
    else:
###@ Need to replace to logg.error
#     print "Unknown config type: %s or ovpn srv IP is not defined. Exiting..." % cfgtype
     sys.exit(1)
    # Tar configs and keys
    # build_tar('example.server.tar.gz', ['client_ca.pem','ta.key','dh'+str(DH_PARAM_SIZE)+'.pem','server_cert.pem','server_cert.key','example.server.conf'])

if __name__ == "__main__":
   banner()
   if len(sys.argv) > 1:
    main(sys.argv[1:])
   else:
###@ Need to replace to help()
    print "Using:"
    print "gen_ovpn.py -n <cert_name>|--name=<cert_name> [--keyca --keytype=server|client|ca --cfgtype=server|client]"
