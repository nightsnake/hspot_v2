#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Category: DB
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

class access_pointsTable(Base):
        __tablename__ = 'access_points'
        id = Column(Integer, primary_key=True)
        name = Column(String(32))
        ip = Column(String(32))
        gw = Column(String(32))
        login = Column(String(40))
        password = Column(String(40))
        hs_id = Column(Integer)
        status = Column(Boolean, default=False)
        url_archive = Column(String(255))
        last_live = Column(TIMESTAMP)
        creat_date = Column(TIMESTAMP)
        comment = Column(String(256))
        current_users = Column(Integer)
        freq = Column(Integer)
        port = Column(Integer)
        type = Column(String(10))
        new = Column(Boolean, default=False)
        done = Column(Integer)

        def __init__(self, login, password, hs_id, status, last_live, creat_date, comment, current_users, freq, type, port,):
            self.id = id
            self.ip = ip
            self.gw = gw
            self.login = login
            self.password = password
            self.hs_id = hs_id
            self.comment = comment
            self.freq = freq
            self.type = type
            self.port = port

        def __repr__(self):
            return "<devices_propertiesTable(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)>" % \
                                            (self.id, self.ip, self.gw, self.login, self.password, self.hs_id, self.url_archive, self.comment, self.freq, self.type, self.port)
class access_pointsAction():
#Get settings by hotspot ID
        def getAPByHspotId(self, hs_id):
            aps = session.query(access_pointsTable).filter_by(hs_id=hs_id).all()
            return aps
#Get settings by ID
        def getAPById(self, id):
            ap = session.query(access_pointsTable).filter_by(id=id).one()
            return ap
#Get list of alive devices
        def getAPAlive(self):
            aliveap = session.query(access_pointsTable).filter_by(status=1).all()
            return aliveap
#Get list of new devices
        def getAPNew(self):
            newap = session.query(access_pointsTable).filter_by(new=1).all()
            return newap
#Set device status to online or offline
        def setApStatus(self, id, status):
            modap = session.query(access_pointsTable).filter_by(id=id).one()
            modap.status = status
            session.commit()
#Set amount of online users on AP
        def setApOnline(self, id, online):
            setonline = session.query(access_pointsTable).filter_by(id=id).one()
            setonline.current_users = current_users
            session.commit()
#Set done
        def setApDone(self, id, done):
            setdone = session.query(access_pointsTable).filter_by(id=id).one()
            setdone.done = done
            session.commit()

        def getHspotIdByAP(self, id):
            hs_id = session.query(access_pointsTable).filter_by(id=id).one()
            return hs_id.hs_id

#Set URL for AP config
        def setAPUrl(self, id, url):
            urlap = session.query(access_pointsTable).filter_by(id=id).one()
            urlap.url_archive = url
            session.commit()
            
