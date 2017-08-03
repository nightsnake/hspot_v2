#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Category: generator
# OpenVPN config and keys generator
# This will generate OpenVPN config and keys.
# Based on OpenVPN keys and config generator by Stuart Morgan <stuart.morgan@mwrinfosecurity.com>
# Copyright 2016 (c) Snake, <snake@nixman.info> @night_snake
# Copyright 2016 (c) Stuart Morgan <stuart.morgan@mwrinfosecurity.com>
##----------------------------------------------------------------------

import os
import sys
import tarfile
import subprocess
import random

from OpenSSL import crypto
from logger import *
from config import Config
from base import *

def ovpncfg():
    config = Config()
    ovpn_cfg = {}
    ovpn_cfg = config.getOVPNConfig()
    return ovpn_cfg

def certcfg(cert_name, cert_type, logger):
 config = Config()
 cert_cfg = config.getCertConfig()
 cert_cfg['commonName'] = "%s" % (cert_name)
# cert_cfg['serial'] = 12345999 #need to add random numbers generator
 cert_cfg['serial'] = int(random.random() * 100000000)
 cert_cfg['cert_filename'] = cert_name + ".pem"
 cert_cfg['cert_key'] = cert_name + ".key"
 
 return cert_cfg    

def build_ca(server_ca,name):
    if os.path.isfile(server_ca['cert_filename']) and os.path.isfile(server_ca['cert_key']):
###@ Need to replace to logg.info
#        sys.stdout.write(colourise("Reusing "+server_ca['cert_filename']+" as the "+name+"\n",'0;36'))
        ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, file(server_ca['cert_filename']).read())
        ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, file(server_ca['cert_key']).read())
###@ Need to replace to logg.info
#        sys.stdout.write(colourise(" "+name+" Fingerprint: "+ca_cert.digest('sha1')+"\n", '0;32'))
    else:
###@ Need to replace to logg.info
#        sys.stdout.write(colourise("Generating new "+name+" CA...",'0;32'))
#        sys.stdout.flush()
        ca_cert, ca_key = generate_ca(server_ca)
###@ Need to replace to logg.info
#        sys.stdout.write(colourise("..done\n",'0;32'))
        open(server_ca['cert_filename'], "w").write(crypto.dump_certificate(crypto.FILETYPE_PEM, ca_cert))
        open(server_ca['cert_key'], "w").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, ca_key))
###@ Need to replace to logg.info
#        sys.stdout.write(colourise(" Written PEM CA certificate to "+server_ca['cert_filename']+"\n", '0;32'))
#        sys.stdout.write(colourise(" Written PEM CA key to "+server_ca['cert_key']+"\n", '0;32'))
#        sys.stdout.write(colourise(" "+name+" Fingerprint: "+ca_cert.digest('sha1')+"\n", '0;32'))
        os.chmod(server_ca['cert_key'], 0600)
    return ca_cert, ca_key

def build_cert(config_cert,ca_cert,ca_key,name):
    if os.path.isfile(config_cert['cert_filename']) and os.path.isfile(config_cert['cert_key']):
###@ Need to replace to logg.info
#        sys.stdout.write(colourise("Reusing "+config_cert['cert_filename']+" as the "+name+" certificate\n",'0;36'))
        cert_cert = crypto.load_certificate(crypto.FILETYPE_PEM, file(config_cert['cert_filename']).read())
        cert_key = crypto.load_privatekey(crypto.FILETYPE_PEM, file(config_cert['cert_key']).read())
###@ Need to replace to logg.info
#        sys.stdout.write(colourise(" SHA1 "+name+" Cert Fingerprint: "+cert_cert.digest('sha1')+"\n", '0;32'))
    else:
###@ Need to replace to logg.info
#        sys.stdout.write(colourise("Generating new "+name+" certificate...",'0;32'))
        sys.stdout.flush()
        cert_req, cert_cert, cert_key = generate_certificate(config_cert,ca_cert,ca_key,name)
###@ Need to replace to logg.info
#        sys.stdout.write(colourise("..done\n",'0;32'))
        open(config_cert['cert_filename'], "w").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert_cert))
        open(config_cert['cert_key'], "w").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, cert_key))
###@ Need to replace to logg.info
#        sys.stdout.write(colourise(" Written PEM certificate to "+config_cert['cert_filename']+"\n", '0;32'))
#        sys.stdout.write(colourise(" Written private key to "+config_cert['cert_key']+"\n", '0;32'))
#        sys.stdout.write(colourise(" SHA1 "+name+" Cert Fingerprint: "+cert_cert.digest('sha1')+"\n", '0;32'))
        os.chmod(config_cert['cert_key'], 0600)
    return cert_cert, cert_key

def build_openssl_extra(DH_PARAM_SIZE):
    if os.path.isfile('ta.key'):
     pass
###@ Need to replace to logg.info
#        sys.stdout.write(colourise("Reusing ta.key\n",'0;36'))
    else:
###@ Need to replace to logg.info
#        sys.stdout.write(colourise("Generating new HMAC key...\n",'0;32'))
        run_cmd(['openvpn','--genkey','--secret','ta.key'])
        os.chmod('ta.key', 0600)
#    sys.stdout.write("\n")

    if os.path.isfile('dh'+str(DH_PARAM_SIZE)+'.pem'):
###@ Need to replace to logg.info
#        sys.stdout.write(colourise("Reusing dh"+str(DH_PARAM_SIZE)+".pem\n",'0;36'))
     pass
    else:
###@ Need to replace to logg.info
#        sys.stdout.write(colourise("Generating DH params...\n",'0;32'))
#        sys.stdout.write("\033[0;90m")
#        sys.stdout.flush()
        run_cmd(['openssl','dhparam','-out','dh'+str(DH_PARAM_SIZE)+'.pem',str(DH_PARAM_SIZE)])
#        sys.stdout.write("\033[0;37m")
#    sys.stdout.write("\n")
#    sys.stdout.flush()

def run_cmd(cmd):
    popen = subprocess.Popen(cmd)
    popen.wait()

def openssl_generate_privatekey(size):
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, size)
    return key

def generate_ca(config_ca):
    ca = crypto.X509()
    ca.set_version(2)
    ca.set_serial_number(config_ca['serial'])
    ca_subj = ca.get_subject()
    if 'commonName' in config_ca:
        ca_subj.commonName = config_ca['commonName']
    if 'stateOrProvinceName' in config_ca:
        ca_subj.stateOrProvinceName = config_ca['stateOrProvinceName']
    if 'localityName' in config_ca:
        ca_subj.localityName = config_ca['localityName']
    if 'organizationName' in config_ca:
        ca_subj.organizationName = config_ca['organizationName']
    if 'organizationalUnitName' in config_ca:
        ca_subj.organizationalUnitName = config_ca['organizationalUnitName']
    if 'emailAddress' in config_ca:
        ca_subj.emailAddress = config_ca['emailAddress']
    if 'countryName' in config_ca:
        ca_subj.countryName = config_ca['countryName']
    if 'validfrom' in config_ca:
        ca.set_notBefore(config_ca['validfrom'])
    if 'validto' in config_ca:
        ca.set_notAfter(config_ca['validto'])
    key = openssl_generate_privatekey(int(config_ca['keyfilesize']))
    ca.add_extensions([
        crypto.X509Extension("basicConstraints", True, "CA:TRUE, pathlen:0"),
        crypto.X509Extension("keyUsage", False, "keyCertSign, cRLSign"),
        crypto.X509Extension("subjectKeyIdentifier", False, "hash", subject=ca),
    ])
    ca.add_extensions([
        crypto.X509Extension("authorityKeyIdentifier", False, "keyid:always",issuer=ca)
    ])
    ca.set_issuer(ca.get_subject())
    ca.set_pubkey(key)
    ca.sign(key, config_ca['hashalgorithm'])
    return ca, key

def generate_certificate(config_cert, ca, cakey, name):
    # Generate the private key
    key = openssl_generate_privatekey(int(config_cert['keyfilesize']))

    # Generate the certificate request
    req = crypto.X509Req()
    req_subj = req.get_subject()
    if 'commonName' in config_cert:
        req_subj.commonName = config_cert['commonName']
    if 'stateOrProvinceName' in config_cert:
        req_subj.stateOrProvinceName = config_cert['stateOrProvinceName']
    if 'localityName' in config_cert:
        req_subj.localityName = config_cert['localityName']
    if 'organizationName' in config_cert:
        req_subj.organizationName = config_cert['organizationName']
    if 'organizationalUnitName' in config_cert:
        req_subj.organizationalUnitName = config_cert['organizationalUnitName']
    if 'emailAddress' in config_cert:
        req_subj.emailAddress = config_cert['emailAddress']
    if 'countryName' in config_cert:
        req_subj.countryName = config_cert['countryName']

    req.set_pubkey(key)
    req.sign(key, config_cert['hashalgorithm'])

    # Now generate the certificate itself
    cert = crypto.X509()
    cert.set_version(2)
    cert.set_serial_number(config_cert['serial'])
    cert.set_subject(req.get_subject())
    cert.set_pubkey(req.get_pubkey())
    cert.set_issuer(ca.get_subject())

    if 'validfrom' in config_cert:
        cert.set_notBefore(config_cert['validfrom'])
    if 'validto' in config_cert:
        cert.set_notAfter(config_cert['validto'])

    if name == 'client':
        usage = 'clientAuth'
        nscerttype = 'client'
    elif name == 'server':
        usage = 'serverAuth'
        nscerttype = 'server'
    else:
        sys.stdout.write("ERROR: Bad certificate type\n")
        sys.exit(1)

    cert.add_extensions([
        crypto.X509Extension("basicConstraints", True, "CA:FALSE"),
        crypto.X509Extension("keyUsage", False, "digitalSignature,keyAgreement"),
        crypto.X509Extension("extendedKeyUsage", False, usage),
        crypto.X509Extension("nsCertType", False, nscerttype),
        crypto.X509Extension("subjectKeyIdentifier", False, "hash", subject=cert),
        crypto.X509Extension("authorityKeyIdentifier", False, "keyid:always", issuer=ca)
    ])

    cert.sign(cakey, config_cert['hashalgorithm'])
    return req, cert, key

def gen_ca(cert_cfg, name, client_key_path, logger):
    cert_cfg['cert_filename'] = "ca.crt"
    cert_cfg['cert_key'] = "ca.key"
    os.chdir( client_key_path )
    ca_cert, ca_key = build_ca(cert_cfg, name)
    return ca_cert, ca_key

def gen_cert(cert_cfg, certype, name, ovpn_path, logger):
    ca_cert = ''
    ca_key = ''
    cert_cert = ''
    cert_key = ''
    client_key_path = ovpn_path + '/keys/'
    retval = os.getcwd()

    # Build the Server and Client CA (if they do not already exist)
    if certype == 'ca':
     ca_cert, ca_key = gen_ca(cert_cfg, 'CA', client_key_path, logger)
#     sys.stdout.write("\n")
    # Build the server and client certificate (signed by the above CAs)
    elif certype == 'server' or certype == 'client':
      ca_cert, ca_key = gen_ca(cert_cfg, 'CA', client_key_path, logger)
      if certype == 'server':
       cert_cfg['cert_filename'] = 'server' + ".pem"
       cert_cfg['cert_key'] = 'server' + ".key"
       os.chdir( client_key_path )
      else:
       cert_cfg['cert_filename'] = name + ".pem"
       cert_cfg['cert_key'] = name + ".key"
       os.chdir( client_key_path )
      cert_cert, cert_key = build_cert(cert_cfg, ca_cert, ca_key, certype)
#      sys.stdout.write("\n")
    else:
###@ Need to replace to logg.error
#     print "Unknown certificate type, exiting"
     sys.exit(2)
    return ca_cert, ca_key, cert_cert, cert_key

def gen_server_config(DH_PARAM_SIZE):
 # Build the server config file
        server_config = open('server.conf', 'w')
        server_config.write("port 1194\n")
        server_config.write("proto tcp\n")
        server_config.write("dev tun\n")
        server_config.write("ca ca.pem\n")
        server_config.write("cert server.pem\n")
        server_config.write("key server.key\n")
        server_config.write("dh dh"+str(DH_PARAM_SIZE)+".pem\n")
        server_config.write("server 10.0.0.0 255.0.0.0\n")
#        server_config.write("topology net30\n")
        server_config.write("ifconfig-pool-persist ipp.txt\n")
        server_config.write("client-config-dir /etc/openvpn/staticlients\n")		
        server_config.write("keepalive 10 120\n")
        server_config.write("cipher AES-128-CBC\n")
        server_config.write("persist-key\n")
        server_config.write("persist-tun\n")
        server_config.write("status openvpn-status.log\n")
        server_config.close()
        # Inform the user
###@ Need to replace to logg.info
#        sys.stdout.write(colourise("Config written to server.conf\n", '0;32'))

def gen_client_config(name, srv_ip, logger):
 # Build the client config file
        client_config = open(name + '.conf', 'w')
        client_config.write("client\n")
        client_config.write("dev tun\n")
        client_config.write("proto tcp\n")
        client_config.write("remote ")
        client_config.write(srv_ip)
        client_config.write(" 1194\n")
        client_config.write("resolv-retry infinite\n")
        client_config.write("nobind\n")
        client_config.write("persist-key\n")
        client_config.write("persist-tun\n")
        client_config.write("ca ca.pem\n")
        client_config.write("cert ")
        client_config.write(name)
        client_config.write(".pem\n")
        client_config.write("key ")
        client_config.write(name)
        client_config.write(".key\n")
        client_config.write("cipher AES-128-CBC\n")
        client_config.close()
        # Inform the user
###@ Need to replace to logg.info
#        sys.stdout.write(colourise("Config written to <client_name>.conf\n", '0;32'))

def gen_staticlients(name, address, server, logger):
        static_path = 'staticlients/'        
        static_config = open(static_path + name, 'w')
        static_config.write("ifconfig-push ")
        static_config.write(address)
        static_config.write(" ")
        static_config.write(server)
        static_config.write("\n")
        static_config.close()
