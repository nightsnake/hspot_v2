#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Make a text banner, colorize text, etc
# Copyright 2016 (c) Snake, <snake@nixman.info> @night_snake
##----------------------------------------------------------------------

import os,sys
import tarfile
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../lib")))
if cmd_subfolder not in sys.path:
 sys.path.insert(0, cmd_subfolder)
from logger import *

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
     except OSError, o:
      logger.warning("Failed to create directory: " + spot.name + ": " + o)
     except SystemError, s:
      logger.warning("Failed to create directory: " + spot.name + ": " + s)
     except RuntimeError, e:
      logger.warning("Failed to create directory: " + spot.name + ": " + e)
     except:
      logger.warning("Failed to create directory: " + spot.name)
    return directory

if __name__ == "__main__":
    banner()
###@Need to add list with functions
