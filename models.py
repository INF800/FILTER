from sqlalchemy import Column, Integer, String, Numeric, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Member(Base):
	"""
	# general
	id :pk
	nick_name: (str)short name
	full_name: (str)complete name
	cur_status: (str)
	bio: (text)
	join_date: (datetime) timestamp cur
	
	# contact
	cur_loc: (str) current location
	twitter_handle: (str)
	linkedin_url: (str)
	whatsapp_num: (str)
	
	#tech/tools details
	prog_langs = {text} coma separated 
	adv_tech = {text} coma separated tech
	med_tech = {text} coma separated tech
	adv_tech = {text} coma separated tech
	
	# secret key - for removing user-self
	secret = {String} case-space-sensitive
	"""
	
	__tablename__ = "Member"
	
	id              = Column(Integer, primary_key=True, index=True)
	nick_name       = Column(String)
	full_name       = Column(String, index=True, nullable=False)
	cur_city        = Column(String)
	cur_status      = Column(String)
	bio             = Column(Text)
	join_date       = Column(DateTime, default=datetime.datetime.utcnow)

	twitter_url     = Column(String)
	linkedin_url    = Column(String)
	whatsapp_num    = Column(String)
	github_url      = Column(String)
	email           = Column(String)
	
	# coma separated
	prog_langs        = Column(Text)
	adv_skills        = Column(Text)
	med_skills        = Column(Text)
	beg_skills        = Column(Text)
	communities       = Column(String)
	fvt_tools         = Column(String)
	
	secret_key      = Column(String, index=True)
	
	# make secret_key and email non nullable