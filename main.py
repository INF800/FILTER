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
	nick_name       : str
	full_name       : str
	cur_status      : str
	cur_city        : str
	bio             : str
	twitter_url     : str
	linkedin_url    : str
	whatsapp_num    : str
	github_url      : str
	email           : str
	
	# coma separated
	communities     : str
	prog_langs      : str
	adv_skills      : str
	med_skills      : str
	beg_skills      : str
	fvt_tools       : str
	
	secret_key      : str


class authMemberRequest(BaseModel):
	secret_key : str
	email      : str
	
	#for.updation
	key        : str = None
	val        : str = None



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
	
	
	

@app.get("/api/dashboard/{json_or_app}")
def dashboard(request: Request, json_or_app="app"):
	"""
	Display summary details of members
	
	returns either temate or json based on query params
	"""
	
	stats = None
	
	context = {
		"request": request,
		"payload": stats
	}
	
	# if template or json
	if json_or_app == "json":
		return {"payload": stats}
	return templates.TemplateResponse("dashboard.html", context)



@app.get("/api/filter/{json_or_app}")
def filter(request: Request, json_or_app="app",db: Session = Depends(get_db)):
	"""
	Explore:
	Display all member details w/ filtering.
	
	return either html template or json based on 
	query params
	"""
	
	mmbr = db.query(Member).all()
	
	context = {
		"request": request,
		"members": mmbr
	}
	
	# template / json
	if json_or_app == "json":
		return {"payload": mmbr}
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
	mmbr.cur_city       = mmbr_req.cur_city
	mmbr.bio            = mmbr_req.bio
	mmbr.communities    = mmbr_req.communities
	mmbr.twitter_url    = mmbr_req.twitter_url
	mmbr.github_url     = mmbr_req.github_url
	mmbr.linkedin_url   = mmbr_req.linkedin_url
	mmbr.whatsapp_num   = mmbr_req.whatsapp_num
	mmbr.email          = mmbr_req.email
	mmbr.prog_langs     = mmbr_req.prog_langs
	mmbr.adv_skills     = mmbr_req.adv_skills
	mmbr.med_skills     = mmbr_req.med_skills
	mmbr.beg_skills     = mmbr_req.beg_skills
	mmbr.fvt_tools      = mmbr_req.fvt_tools
	mmbr.secret_key     = mmbr_req.secret_key

	db.add(mmbr)
	db.commit()
	
	return None
	


@app.delete("/api/member")
def remove_members(mmbr_req: authMemberRequest, db: Session = Depends(get_db)):
	"""
	Remove entry wrt `secretkey` & `full name` from db
	"""
	
	secret_key = mmbr_req.secret_key
	email      = mmbr_req.email
	
	mmbr = db.query(Member).filter(Member.secret_key==secret_key and Member.email==email).first()
	
	if mmbr is None:
		status = "secret key or email don't match"
	else:
		db.delete(mmbr)
		db.commit()
		status = "success"
		
	return {"status": status}


	
@app.patch("/api/member")
def update_members(mmbr_req: authMemberRequest, db: Session = Depends(get_db)):
	"""
	alter values for an entry after verification
	"""
	
	secret_key = mmbr_req.secret_key
	email = mmbr_req.email
	mmbr = db.query(Member).filter(Member.secret_key==secret_key and Member.email==email).first()
	
	if mmbr is None:
		status = "secret key or email don't match"
	else:
		
		# take key where we need to update and value to 
		# which we have to update
		key = mmbr_req.key
		val = mmbr_req.val
		
		#mmbr.key = val (key is str)
		if key == "nick_name":
			mmbr.nick_name = val
		if key == "full_name":
			mmbr.full_name = val
		if key == "cur_status":
			mmbr.cur_status = val
		if key == "cur_city":
			mmbr.cur_city = val
		if key == "bio":
			mmbr.bio = val
		if key == "twitter_url":
			mmbr.twitter_url = val
		if key == "linkedin_url":
			mmbr.linkedin_url = val
		if key == "whatsapp_num":
			mmbr.whatsapp_num = val
		if key == "github_url":
			mmbr.github_url = val
		if key == "email":
			mmbr.email = email
		if key == "communities":
			mmbr.communities = val
		if key == "prog_langs":
			mmbr.prog_langs = val
		if key == "adv_skills":
			mmbr.adv_skills = val
		if key == "med_skills":
			mmbr.med_skills = val
		if key == "beg_skills":
			mmbr.beg_skills = val
		if key == "fvt_tools":
			mmbr.fvt_tools = val
		if key == "secret_key":
			mmbr.secret_key = val
		
		
		db.add(mmbr)
		db.commit()
		status = "success!"
		
	return {"status": status}
# ----------------------------------------
# end
# ----------------------------------------