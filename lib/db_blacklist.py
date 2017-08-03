#!/usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
# Category: DB
# Table and methods for table 'black_sites'
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

class blacklistTable(Base):
        __tablename__ = 'black_site'
        id = Column(Integer, primary_key=True)
        site = Column(String(255))
        comments = Column(String(100))
        id_device = Column(Integer)
        def __init__(self, id_device, site, comments):
                self.id_device = id_device
                self.site = site
                self.comment = comments
        def __repr__(self):
                return "<devTable(%s, %s, %s, %s, )>" % \
                       (self.id, self.site, sefl.comments, self.id_device)

class blacklistAction():
        def getSitesByDevId(self,id):
            idhspot = session.query(blacklistTable).filter_by(id_device=id).all()
            return idhspot
