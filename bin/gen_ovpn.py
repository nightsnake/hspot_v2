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
    # Now give instructions
    sys.stdout.write(colourise("On the OpenVPN Server:\n",'0;40'))
    sys.stdout.write(colourise("ca client_ca.pem\n",'0;32'))
    sys.stdout.write(colourise("cert server.pem\n",'0;32'))
    sys.stdout.write(colourise("key server.key\n",'0;32'))
    sys.stdout.write("\n")
    sys.stdout.write(colourise("On the OpenVPN Client:\n",'0;40'))
    sys.stdout.write(colourise("ca server_ca.pem\n",'0;32'))
    sys.stdout.write(colourise("cert client.pem\n",'0;32'))
    sys.stdout.write(colourise("key client.key\n",'0;32'))
    sys.stdout.write("\n")

def main(argv):
    cert_cfg = {}
    certname = ''
    certype = ''
    cfgtype = ''
    ovpn_path = '/etc/openvpn'
    client_key_path = ovpn_path + '/easy-rsa/keys'

    try:
      opts, args = getopt.getopt(argv,"hn:k:c:",["name=","keytype=","cfgtype="])
    except getopt.GetoptError:
      print 'Unkown option'
      print 'gen_ovpn.py -n <cert_name>|--name=<cert_name> [--keyca --keytype=server|client|ca --cfgtype=server|client]'
      sys.exit(2)
    except Exception as e:
        sys.stdout.write("Error: %s\n" % e)
        sys.exit(1)
    for opt, arg in opts:
      if opt == '-h':
         print 'gen_ovpn.py -n <cert_name>|--name=<cert_name> [--keytype=server|client|ca --cfgtype=server|client]'
         sys.exit()
      elif opt == '-n' or opt == '--name':
         certname = arg
      elif opt == '-k' or opt == '--keytype':
         certype = arg
      elif opt == '-c' or opt == '--cfgtype':
         cfgtype = arg
      else:
         print "Unknown option: %s" % opt
         sys.exit(1)
    # Make a certconfig
    cert_cfg = certcfg(certname, certype)
    # Get keys (CA, Server or Client)
    ca_cert, ca_key, cert_cert, cert_key = gen_cert(cert_cfg, certype, certname)

    # Now build ta.key and dh params if they do not already exist
    build_openssl_extra()
    sys.stdout.write("\n")
    # Get some manual to user
    instructions()

if __name__ == "__main__":
   banner()
   if len(sys.argv) > 1:
    main(sys.argv[1:])
   else:
    print "Using:"
    print "gen_ovpn.py -n <cert_name>|--name=<cert_name> [--keyca --keytype=server|client|ca --cfgtype=server|client]"
