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
	professional: (bool) working/student
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
	emp_role        = Column(Boolean)
	bio             = Column(Text)
	portfolio       = Column(String)
	join_date       = Column(DateTime, default=datetime.datetime.utcnow)
	
	community       = Column(String, nullable=False)
	cur_city				= Column(String)
	twitter_handle  = Column(String)
	linkedin_url    = Column(String)
	whatsapp_num    = Column(String, nullable=True)
	github_uname    = Column(String)
	
	# coma separated
	interests         = Column(String)
	prog_langs        = Column(Text)
	adv_skills        = Column(Text)
	med_skills        = Column(Text)
	beg_skills        = Column(Text)
	
	secret_key      = Column(String, index=True)