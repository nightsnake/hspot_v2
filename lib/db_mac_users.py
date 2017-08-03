#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Table and methods for table 'mac_users'
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

class macTable(Base):
        __tablename__ = 'mac_users'
        user_id = Column(Integer, primary_key=True)
        device_id = Column(Integer)
        mac_addr = Column(TEXT)
        comment = Column(TEXT)
        creat_date = Column(TIMESTAMP)
        def __init__(self, user_id, device_id, mac_addr, comment):
                self.user_id = user_id
                self.device_id = device_id
                self.mac_addr = mac_addr
                self.comment = comment
        def __repr__(self):
                return "<macTable(%s, %s, %s, %s, %s)>" % (self.user_id, self.device_id, self.mac_addr, self.comment, self.creat_date)

class macAction():
        def getUsersbyDevice(self, device_id):
            users = session.query(macTable).filter_by(device_id=device_id).all()
            return users
        def getDevicebyUser(self, user_id):
            device = session.query(macTable).filter_by(user_id=user_id).one()
            return device.device_id
        def getUserbyID(self, user_id):
            user = session.query(macTable).filter_by(user_id=user_id).one()
            return user
        def getMACbyID(self, user_id):
            user = session.query(macTable).filter_by(user_id=user_id).one()
            mac = user.mac_addr
            return mac

