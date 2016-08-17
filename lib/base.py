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

def build_zip(filename,includedfiles):
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
