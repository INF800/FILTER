# ----------------------------------------
# create fastapi app 
# ----------------------------------------
from fastapi import FastAPI
app = FastAPI()


# ----------------------------------------
# setup templates folder
# ----------------------------------------
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")


# ----------------------------------------
# setup db
# ----------------------------------------
import models
from sqlalchemy.orm import Session
from database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine) #creates tables
# stocks db will appear once you run uvicorn.
# get into sqlite and try `.schema`
from models import Member


# ----------------------------------------
# import custom modules
# ----------------------------------------


# ----------------------------------------
# dependency injection
# ----------------------------------------
from fastapi import Depends

def get_db():
	""" returns db session """
	
	try:
		db = SessionLocal()
		yield db
	finally:
		db.close


# ----------------------------------------
# bg tasks
# ----------------------------------------


# ----------------------------------------
# define structure for requests (Pydantic & more)
# ----------------------------------------
from fastapi import Request # for get
from pydantic import BaseModel # for post

class MemberRequest(BaseModel):
	id              : str
	nick_name       : str
	full_name       : str
	cur_status      : bool
	bio             : str
	link2self       : str
	
	community       : str
	cur_city				: str
	twitter_handle  : str
	linkedin_url    : str
	whatsapp_num    : str	
	github_uname    : str
	
	# coma separated
	prog_langs      : str
	adv_skills      : str
	med_skills      : str
	beg_skills      : str
	
	secret_key      : str


# ----------------------------------------
# ----------------------------------------
# routes and related funcs
# ----------------------------------------
# ----------------------------------------
@app.get("/")
def home(request: Request):
	"""
	dashboard / add+remove / filter
	"""
	
	context = {
		"request": request
	}
	
	return templates.TemplateResponse("home.html", context)



@app.get("/form")
def add_or_remove_members(request: Request):
	"""
	form to add/remove members
	"""
	context = {
		"request": request
	}
	return templates.TemplateResponse("addrem.html", context)
	
	
	

@app.get("/api/dashboard")
def dashboard(request: Request):
	"""
	Display summary details of members
	"""
	
	payload = None
	
	context = {
		"request": request,
		"payload": payload
	}
	
	# if template or json
	return templates.TemplateResponse("dashboard.html", context)



@app.get("/api/filter")
def filter(request: Request):
	"""
	Explore:
	Display all member details w/ filtering.
	"""
	
	payload = None
	
	context = {
		"request": request,
		"payload": payload
		
	}
	
	# if template or json
	return templates.TemplateResponse("filter.html", context)



@app.post("/api/member")
def add_members(mmbr_req: MemberRequest, db: Session = Depends(get_db)):
	"""
	adds user details to db
	"""
		
	mmbr = Member()
	mmbr.full_name      = mmbr_req.full_name
	mmbr.nick_name      = mmbr_req.nick_name
	mmbr.cur_status     = mmbr_req.cur_status
	mmbr.bio            = mmbr_req.bio
	mmbr.link2self      = mmbr_req.link2self
	mmbr.community      = mmbr_req.community
	mmbr.cur_city       = mmbr_req.cur_city
	mmbr.twitter_handle = mmbr_req.twitter_handle
	mmbr.github_uname   = mmbr_req.github_uname
	mmbr.linkedin_url   = mmbr_req.linkedin_url
	mmbr.whatsapp_num   = mmbr_req.whatsapp_num
	mmbr.prog_langs     = mmbr_req.prog_langs
	mmbr.adv_skills     = mmbr_req.adv_skills
	mmbr.med_skills     = mmbr_req.med_skills
	mmbr.beg_skills     = mmbr_req.beg_skills
	mmbr.secret_key     = mmbr_req.secret_key

	db.add(mmbr)
	db.commit()
	
	return None
	


# edit based on secret key as well <<<<<

@app.delete("/api/member")
def remove_members(mmbr_req: MemberRequest, db: Session = Depends(get_db)):
	"""
	Remove entry wrt `secretkey` & `full name` from db
	"""
	
	return None



# ----------------------------------------
# end
# ----------------------------------------