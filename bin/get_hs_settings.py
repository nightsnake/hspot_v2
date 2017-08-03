#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Category: monitoring
# Get hspot settings (ssid, freq...)
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
import yaml

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
engine = create_engine('mysql://'+dbuser+':'+dbpass+'@'+dbhost+':'+dbport+'/'+dbname, echo=False)
conn = engine.connect()

hs_id = conn.execute("SELECT %s FROM %s WHERE %s = %s" % ('id', hs_table, 'status', 1)).fetchall()
for i in hs_id:
#  ap_id = conn.execute("SELECT %s FROM %s WHERE %s = %s AND %s = 0" % ('id', ap_table, 'hs_id', hs_id[0], 'done')).fetchone()

#to_yaml = {'trunk':trunk_template, 'access':access_template}
#with open('sw_templates.yaml', 'w') as f:
#    f.write(yaml.dump(to_yaml, default_flow_style=False))

#with open('sw_templates.yaml') as f:
#    print f.read()
