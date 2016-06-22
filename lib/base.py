#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Make a text banner, colorize text, etc
# Copyright 2016 (c) Snake, <snake@nixman.info> @night_snake
##----------------------------------------------------------------------

import sys

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

if __name__ == "__main__":
    banner()
