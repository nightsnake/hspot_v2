#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Database module base.py
# Copyright (C) Snake, 2015
##----------------------------------------------------------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import update
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.dialects.mysql import TEXT
import ConfigParser, os, sys

script_dir = os.path.dirname(__file__)
rel_path = "../etc/base.cfg"
abs_file_path = os.path.join(script_dir, rel_path)

config = ConfigParser.ConfigParser()
config.read(abs_file_path)

#### Database user credentials
hostname  = config.get('DB', 'hostname')
dbname    = config.get('DB', 'dbname')
dbuser    = config.get('DB', 'dbuser')
dbpass    = config.get('DB', 'dbpass')
dbhost    = config.get('DB', 'dbhost')
dbport    = config.get('DB', 'dbport') 
####

engine = create_engine('mysql://'+dbuser+':'+dbpass+'@'+dbhost+':'+dbport+'/'+dbname, echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

def main():
    pass

if __name__ == "__main__":
    sys.exit(main())
