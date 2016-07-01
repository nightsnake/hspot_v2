#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Table and methods for table 'devices_properties'
# Copyright (C) Snake, 2015
##----------------------------------------------------------------------

#### SQLAlchemy ####
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import update
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.dialects.mysql import TEXT
#### ---------- ####
from DB import *

class devices_propertiesTable(Base):
        __tablename__ = 'devices_properties'
        id = Column(Integer, primary_key=True)
        trial_type = Column(Integer)
        trial_uptime = Column(Integer)
        trial_timeout = Column(Integer)
        id_device = Column(Integer)
        captive_apple = Column(Boolean, default=False)
        captive_android = Column(Boolean, default=False)
        captive_win = Column(Boolean, default=False)
        social = Column(String(100))
        def __init__(self, id, trial_type, trial_uptime, trial_timeout, id_device):
            self.id = id
            self.trial_type = trial_type
            self.self.trial_uptime = trial_uptime
            self.trial_timeout = trial_timeout
            self.id_device = id_device
        def __repr__(self):
            return "<devices_propertiesTable(%s, %s, %s, %s, %s)>" % (self.id, self.trial_type, self.trial_uptime, self.trial_timeout, self.id_device)
class devices_propertiesAction():
#Get settings by ID
        def getSettingsById(self, id_device):
            settings = session.query(devices_propertiesTable).filter_by(id_device=id_device).one()
            return settings
