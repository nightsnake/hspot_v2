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

def ovpn_generator(certname, certype, cfgtype, srv_ip, cli_ip, logger):
    """
    function for external calls (unattended)
    """
    retval = os.getcwd()
    ovpn_cfg = ovpncfg()
    ovpn_path = ovpn_cfg['ovpn_path']
    ovpn_srv = ovpn_cfg['ovpn_srv']
    key_outpath = ovpn_cfg['key_outpath']
    key_path = ovpn_path + '/keys/'
    client_key_path = ovpn_path + '/keys/'
    DH_PARAM_SIZE = ovpn_cfg['DH_PARAM_SIZE']

    if (certype == 'server' or certype == 'client') and certname:
     logger.debug("Make cert  %s" % certname)
     os.chdir( key_path )
     # Now build ta.key and dh params if they do not already exist
     build_openssl_extra(DH_PARAM_SIZE)
     # Make a certconfig
     cert_cfg = certcfg(certname, certype, logger)
     # Make keys (CA, Server or Client)
     ca_cert, ca_key, cert_cert, cert_key = gen_cert(cert_cfg, certype, certname, ovpn_path, logger)
     # Make static ip for client, if defined
     if certype == 'client' and cli_ip:
      logger.debug("Type of cert is client and ip is %s" % cli_ip)
      os.chdir( ovpn_path )
      logger.debug("Make staticfile for %s" % cli_ip)
      gen_staticlients(cert_cfg['commonName'], cli_ip, ovpn_srv, logger)
      inpath = client_key_path
      outpath = key_outpath + '/' + certname
      logger.debug("Copy keys to directory with user configs. In: %s, out: %s" % (inpath, outpath))
      copyFile(certname + '.crt', inpath, outpath)
      copyFile(certname + '.key', inpath, outpath)

    elif certype:
      logger.error("Fatal error: unknown cert type or undefined certname")
      return -1
     
    # Make configs for client and server
    if cfgtype == 'server':
     os.chdir( ovpn_path )
     gen_server_config(DH_PARAM_SIZE)
    elif cfgtype == 'client' and srv_ip:
     os.chdir( retval + '/../tmp')
     gen_client_config(certname, srv_ip, logger)
     os.chdir( retval )
    elif cfgtype:
     logger.error("Unknown config type: %s or ovpn srv IP is not defined. Exiting..." % cfgtype)
     return -1

    return 1

def help():
#Help for standalone usage
    pass

def main(argv, logger):
    """
    Main call. Interactive output
    """
    cert_cfg = {}
    certname = ''
    certype = ''
    cfgtype = ''
    cli_ip = ''
    srv_ip = ''
    retval = os.getcwd()
    ovpn_cfg = ovpncfg()
    ovpn_path = ovpn_cfg['ovpn_path']
    ovpn_srv = ovpn_cfg['ovpn_srv']
    key_outpath = ovpn_cfg['key_outpath']
    DH_PARAM_SIZE = ovpn_cfg['DH_PARAM_SIZE']
    client_key_path = ovpn_path + '/keys/'

    try:
###@If verbose defined, show logs on screen
      opts, args = getopt.getopt(argv,"hvn:k:c:a:s:",["name=","keytype=","cfgtype=", "address=", "server=", "verbose", "help"])
    except getopt.GetoptError as e:
#      print 'Unkown option'
###@ Need to add help() with information about keys and options
      print 'gen_ovpn.py -n <cert_name>|--name=<cert_name> [--keyca] --keytype=server|client|ca --cfgtype=server|client --address=10.0.1.1]'
      logger.error("Unknown option: %s" % e)
      sys.exit(2)
    except Exception as e:
        logger.error("Error: %s\n" % e)
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
         logger.error("Unknown option: %s" % opt)
         sys.exit(1)
    if certype:
     # Make a certconfig
     cert_cfg = certcfg(certname, certype, logger)
 
     # Get keys (CA, Server or Client)
     ca_cert, ca_key, cert_cert, cert_key = gen_cert(cert_cfg, certype, certname, ovpn_path, logger)
     # Now build ta.key and dh params if they do not already exist
     os.chdir( ovpn_path )
     if certype == 'client' and cli_ip:
      gen_staticlients(cert_cfg['commonName'], cli_ip, ovpn_srv, logger)
      logger.debug("Copying certificate and key to user folder")
      inpath = ovpn_path
      outpath = key_outpath + '/' + certname
      copyFile(certname + '.pem', inpath, outpath)
      copyFile(certname + '.key', inpath, outpath)
      build_openssl_extra(DH_PARAM_SIZE)
      sys.stdout.write("\n")
      # Get some manual to user
      instructions()
    # Make configs for client and server
    if cfgtype == 'server':
     os.chdir( client_key_path )
     gen_server_config(DH_PARAM_SIZE)
    elif cfgtype == 'client' and srv_ip:
     tmp_dir = retval + '/../tmp'
     os.chdir( tmp_dir )
     gen_client_config(certname, srv_ip, logger)          
    else:
     logger.error("Unknown config type: %s or ovpn srv IP is not defined. Exiting..." % cfgtype)
     sys.exit(1)
    # Tar configs and keys
    # build_tar('example.server.tar.gz', ['client_ca.pem','ta.key','dh'+str(DH_PARAM_SIZE)+'.pem','server_cert.pem','server_cert.key','example.server.conf'])

if __name__ == "__main__":
   banner()
   logger = logger("ovpn-generator")
#   logger.debug("AP ID: " + id)
   if len(sys.argv) > 1:
    logger.debug("Starting program with option %s" % sys.argv[1:])
    main(sys.argv[1:], logger)
   else:
###@ Need to replace to help()
    print "Using:"
    print "gen_ovpn.py -n <cert_name>|--name=<cert_name> [--keyca --keytype=server|client|ca --cfgtype=server|client]"
