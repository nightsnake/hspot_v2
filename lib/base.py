#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Category: base functions
# Make a text banner, colorize text, etc
# Copyright 2016 (c) Snake, <snake@nixman.info> @night_snake
##----------------------------------------------------------------------

import os,sys,inspect
from os.path import basename
import tarfile
import zipfile
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../lib")))
if cmd_subfolder not in sys.path:
 sys.path.insert(0, cmd_subfolder)
from logger import *

def addAddressToInt(c, device, port, address, logger):
 try:
  if device.type == 'mkt': #check AP type
###@need to add check for existing address
   ip = c.response_handler(c.talk(["/ip/address/add",
                                                              "=address="+address,
                                                              "=interface="+port,
                                ]))
   logger.debug("IP address %s has been added to interface %s" % (address, port))
  else:
   logger.warning("Unknown device type %s for %s" % (device.type, device.name))
   return 0
 except Exception as e:
  logger.error("[addAddressToInt] Unexpected error: %s" % e)
  return -1

def addPortToBridge(c, device, port, bridge, logger):
#Universal func for adding port to bridge
 try:
  if (device.type == 'mkt' and isPortInBridge(c, device, port, bridge, logger) == 0): #check AP type
   br = c.response_handler(c.talk(["/interface/bridge/port/add",
                                                              "=interface="+port,
                                                              "=bridge="+bridge,
                                ]))
   logger.debug("Interface %s was successfully added to bridge %s on device %s" % (port, bridge, device.name))
  else:
   logger.warning("Unknown device type %s for %s" % (device.type, device.name))
   return 0
 except Exception as e:
  logger.error("[addPortToBridge] Unexpected error: %s" % e)
  return -1

def delPortFromBridge(c, device, port, bridge, logger):
#Universal func for adding port to bridge
 try:
  if (device.type == 'mkt' and isPortInBridge(c, device, port, bridge, logger) == 1): #check AP type
   ports = c.response_handler(c.talk(["/interface/bridge/port/print", "?interface="+str(port),]))
   br = c.response_handler(c.talk(["/interface/bridge/port/remove",
                                                              "=.id="+ports[0]['.id'],
                                ]))
   logger.debug("Interface %s was successfully removed from bridge %s on device %s" % (port, bridge, device.name))
  else:
   logger.warning("Unknown device type %s for %s" % (device.type, device.name))
   return 0
 except Exception as e:
  logger.error("[delPortFromBridge] Unexpected error: %s" % e)
  return -1

def isPortInBridge(c, device, port, bridge, logger):
#Universal func for adding port to bridge
 try:
  if device.type == 'mkt': #check AP type
   ports = c.response_handler(c.talk(["/interface/bridge/port/print", "?interface="+str(port),]))
   logger.debug("Check if interface %s in bridge %s on device %s. Result: %s" % (port, bridge, device.name, ports))   
   if ports:
    logger.debug("Interface %s was found in bridge %s on device %s" % (port, bridge, device.name))   
    return 1
   else:
    logger.debug("Interface %s was not found in bridge %s on device %s" % (port, bridge, device.name))
    return 0
  else:
   logger.warning("Unknown device type %s for %s" % (device.type, device.name))
   return 0
 except Exception as e:
  logger.error("[isPortInBridge] Unexpected error: %s" % e)
  return -1

def banner():
    sys.stdout.write("\n")
    sys.stdout.write("      ______             _           \n")
    sys.stdout.write("     / _____)           | |          \n")
    sys.stdout.write("    ( (____  ____  _____| |  _ _____ \n")
    sys.stdout.write("     \____ \|  _ \(____ | |_/ ) ___ |\n")
    sys.stdout.write("     _____) ) | | / ___ |  _ (| ____|\n")
    sys.stdout.write("    (______/|_| |_\_____|_| \_)_____)\n")
    sys.stdout.write("\n")
    sys.stdout.write("OpenVPN config and keys generator (server/client\n")
    sys.stdout.write("    Snake <snake@nixman.info> | @night_snake\n")
    sys.stdout.write("\n")
    sys.stdout.flush()

def colourise(string,colour):
    return "\033["+colour+"m"+string+"\033[0m"

def build_tar(filename,includedfiles):
    tar = tarfile.open(filename, "w:gz")
    for name in includedfiles:
        tar.add(name)
    tar.close()

def build_zip(filename,includedfiles, logger):
    try:
     logger.debug("Create zip archive")
     zip = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
     for f in includedfiles:
      logger.debug("Add %s to archive" % basename(f))
      zip.write(f, basename(f))
     zip.close()
    except Exception as e:
     logger.warning("Failed to create archive %s: %s" % (filename, e))


def filelist (directory):
    """
    Get filelist from directory
    """
    import os
    from os import path
    files = []
    files = os.listdir(directory)
    sorted_files = sorted(files)

    return sorted_files

def mkdir (directory, logger):
    if not os.path.exists(directory):
     try:
      os.makedirs(directory)
     except Exception as e:
      logger.warning("Failed to create directory %s: %s" % (spot.name, e))
    return directory

def copyFile(name, inpath, outpath):
        from shutil import copyfile
        src = inpath + '/' + name
        dst = outpath + '/' + name
        copyfile(src, dst)

if __name__ == "__main__":
    banner()
###@Need to add list with functions
