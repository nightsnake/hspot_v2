#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Table and methods for table 'devices'
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

#Main table with hspot properties
class devTable(Base):
        __tablename__ = 'devices'
        id = Column(Integer, primary_key=True)
        name = Column(String(32))
        ip = Column(String(32))
        gw = Column(String(32))
        status = Column(Boolean, default=False)
        server = Column(String(32))
        secret = Column(String(128))
        ssid = Column(String(32))
        login = Column(String(32))
        password = Column(String(32))
        network = Column(String(32))
        service_ssid = Column(String(32))
        service_hide = Column(Boolean, default=False)
        service_encryption  = Column(Boolean, default=False)        
        service_pass = Column(String(32))
        site = Column(String(255))
        last_live = Column(TIMESTAMP)
        creat_date = Column(TIMESTAMP)
        comment = Column(String(256))
        new = Column(Boolean, default=False)
        current_users = Column(Integer)
        url_archive = Column(String(255))
        def __init__(self, name, ip, gw, server, secret, ssid, login, password, network, site, comment):
                self.name = name
                self.ip = ip
                self.gw = gw
                self.server = server
                self.secret = secret
                self.ssid = ssid
                self.login = login
                self.password = password
                self.network = network
                self.site = site
                self.comment = comment
        def __repr__(self):
                return "<devTable(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,)>" % \
                       (self.id, self.name, self.ip, self.gw, self.status, self.server, self.secret, self.ssid, self.service_ssid, self.service_hide, self.service_encryption, self.service_pass,
                        self.login, self.password, self.network, self.site, self.last_live, self.creat_date, self.current_users, self.comment, self.url_archive)

class devAction():
### 'Set' functions
#Set device status to online or offline
        def devSetStatus(self, id, status):
            modhspot = session.query(devTable).filter_by(id=id).one()
            modhspot.status = status
            session.commit()
#Set device as new
        def devSetNew(self, id):
            acthspot = session.query(devTable).filter_by(id=id).one()
            acthspot.new = 1
            session.commit()
#Set 'online' (current users, connected to wifi)
        def devSetOnline(self, id, current_users):
            modhspot = session.query(devTable).filter_by(id=id).one()
            modhspot.current_users = current_users
            session.commit()
#Set config URL for hspot
        def devSetConfigURL(self, id, url):
            urlhspot = session.query(devTable).filter_by(id=id).one()
            urlhspot.url_archive = url
            session.commit()

### 'Get' functions
#Get devices with new=1
        def devGetNew(self):
            newspot = session.query(devTable).filter_by(new=1).all()
            return newspot
#Get list with all devices
        def devGetAll(self):
            hspots = session.query(devTable).all()
            return hspots
#Get list of alive devices
        def devGetAlive(self):
            alivespot = session.query(devTable).filter_by(status=1).all()
            return alivespot
#Get hspot object by his ID
        def devGetById(self,id):
            idhspot = session.query(devTable).filter_by(id=id).one()
            return idhspot

