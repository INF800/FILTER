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
	
	# personal
	id              = Column(Integer, primary_key=True, index=True)
	nick_name       = Column(String)
	full_name       = Column(String, index=True, nullable=False)
	cur_city        = Column(String)
	cur_status      = Column(String)
	bio             = Column(Text)
	communities     = Column(Text) # coma sep
	join_date       = Column(DateTime, default=datetime.datetime.utcnow)
	
	# social
	twitter_url     = Column(String)
	linkedin_url    = Column(String)
	whatsapp_num    = Column(String)
	github_url      = Column(String)
	email           = Column(String, nullable=False, index=True, unique=True)
	
	# skills
	dom_1          = Column(String)
	dom_2          = Column(String)
	dom_3          = Column(String)
	dom_4          = Column(String)
	dom_5          = Column(String)
	dom_6          = Column(String)
	dom_7          = Column(String)
	dom_8          = Column(String)
	dom_1skill     = Column(String)
	dom_1interest  = Column(String)
	dom_2skill     = Column(String)
	dom_2interest  = Column(String)
	dom_3skill     = Column(String)
	dom_3interest  = Column(String)
	dom_4skill     = Column(String)
	dom_4interest  = Column(String)
	dom_5skill     = Column(String)
	dom_5interest  = Column(String)
	dom_6skill     = Column(String)
	dom_6interest  = Column(String)
	dom_7skill     = Column(String)
	dom_7interest  = Column(String)
	dom_8skill     = Column(String)
	dom_8interest  = Column(String)
	
	secret_key      = Column(String, index=True, nullable=False)