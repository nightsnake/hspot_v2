#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Category: DB
# Table and methods for table 'user_profiles'
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
from Base import *

class profileTable(Base):
        __tablename__ = 'user_profiles'
        profile_id = Column(Integer, primary_key=True)
        device_id = Column(Integer)
        type = Column(Boolean, default=False)
        name = Column(String(32))
        idle_timeout = Column(String(32))
        dead_timeout = Column(String(32))
        session_timeout = Column(String(32))
        rate = Column(String(32))
        def __init__(self, profile_id, device_id, type, name, idle_timeout, dead_timeout, session_timeout, rate):
            self.profile_id = profile_id
            self.device_id = device_id
            self.type = type
            self.name = name
            self.idle_timeout = idle_timeout
            self.dead_timeout = dead_timeout
            self.session_timeout = session_timeout
            self.rate = rate
        def __repr__(self):
                return "<profileTable(%s, %s, %s, %s, %s, %s, %s, %s)>" % (self.profile_id, self.device_id, self.type, self.name, self.idle_timeout, self.dead_timeout, self.session_timeout, self.rate)

class profileAction():
        def getProfilesbyDevice(self, device_id):
            profiles = session.query(profileTable).filter_by(device_id=device_id).all()
            return profiles
        def getDeviceIdbyProfile(self, profile_id):
            device = session.query(profileTable).filter_by(profile_id=profile_id).one()
            return device.device_id
        def getProfilebyID(self, profile_id):
            profile = session.query(profileTable).filter_by(profile_id=profile_id).one()
            return profile

