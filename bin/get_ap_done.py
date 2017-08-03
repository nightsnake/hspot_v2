#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Category: monitoring
# Check DB for unprovisioned AP
# Return first ap_id which have done == 0 and hs.status == 1
# Copyright (C) Snake, 2017
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
hs_table = 'devices'
ap_table = 'access_points'
hs_status = 0
hs_id = 0
ap_id = []
engine = create_engine('mysql://'+dbuser+':'+dbpass+'@'+dbhost+':'+dbport+'/'+dbname, echo=False)
conn = engine.connect()
hs_id = conn.execute("SELECT %s FROM %s WHERE %s = %s" % ('id', hs_table, 'status', 1)).fetchone()
ap_id = conn.execute("SELECT %s FROM %s WHERE %s = %s AND %s = 0" % ('id', ap_table, 'hs_id', hs_id[0], 'done')).fetchone()
if ap_id:
 print ap_id[0]
