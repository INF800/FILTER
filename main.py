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
	
	 # personal
	 nick_name       : str
	 full_name       : str
	 cur_status      : str
	 cur_city        : str
	 bio             : str
	 communities     : str
	 
	 # social
	 twitter_url     : str
	 linkedin_url    : str
	 whatsapp_num    : str
	 github_url      : str
	 email           : str
	 
	 # coma separated
	 dom_1          : str
	 dom_2          : str
	 dom_3          : str
	 dom_4          : str
	 dom_5          : str
	 dom_6          : str
	 dom_7          : str
	 dom_8          : str
	 dom_1skill     : str
	 dom_1interest  : str
	 dom_2skill     : str
	 dom_2interest  : str
	 dom_3skill     : str
	 dom_3interest  : str
	 dom_4skill     : str
	 dom_4interest  : str
	 dom_5skill     : str
	 dom_5interest  : str
	 dom_6skill     : str
	 dom_6interest  : str
	 dom_7skill     : str
	 dom_7interest  : str
	 dom_8skill     : str
	 dom_8interest  : str
	 
	 secret_key     : str


class authMemberRequest(BaseModel):
	secret_key : str
	email      : str
	
	#for updation (field, field_val)
	key        : str = None
	val        : str = None
	val_type   : str = "str"



# ----------------------------------------
# ----------------------------------------
# routes and related funcs
# ----------------------------------------
# ----------------------------------------
@app.get("/")
def home(request: Request):
	"""
	Render simple UI for home.
	"""
	
	context = {
		"request": request
	}
	
	return templates.TemplateResponse("home.html", context)



@app.get("/form")
def add_patch_remove_members(request: Request):
	"""
	Render a form through which user can interact
	with the API.
	It uses Axios and performs POST, DELETE and PATCH
	operations using clientside js
	"""
	context = {
		"request": request
	}
	return templates.TemplateResponse("addrem.html", context)
	
	
	

@app.get("/api/dashboard/{json_or_app}")
def dashboard(request: Request, json_or_app="app", db: Session = Depends(get_db)):
	"""
	Display summary details of the whole platform and 
	the enlisted Members.
	
	Query parameter `json_or_app` supports one of either two values - `json`
	or `app`
	
	- `/api/dashboard/app` renders UI 
	- `/api/dashboard/json` returns JSON response payload
	with key stats which can be used by any client to visualize
	
	ChartJS is used in this UI to visualize stats.
	"""
	
	stats = None
	mmbrs = db.query(Member).all()
	n_mmbrs = db.query(Member).count()
	print(n_mmbrs)
	col_names = Member.__table__.columns.keys()
	print(col_names)
	
	# number of people vs skills - interested, skilled
	"""
	# double line graph
	
	# xaxis -skills
	# yaxis -n_ppl
	# lines - interested,n actual skill
	"""
	
	# nop vs loc
	"""
	# piechart
	"""
	
	# piechart - working vs stud
	"""
	# dougnut
	"""
	
	# nop vs dev vs others communities
	"""
	horizonta graph
	
	yaxis -communities
	xaxis -nop
	bars -students, working, other, top2 major domains
	"""
	
	#skilled/Total Members Ratio (In filter)
	"""
	x-axis domain
	yaxis ratio
	"""
	
	# domain wise
	"""
	"""
	
	context = {
		"request": request,
		"payload": stats
	}
	
	# if template or json
	if json_or_app == "json":
		return {"payload": stats}
	return templates.TemplateResponse("dashboard.html", context)



@app.get("/api/filter/{json_or_app}")
def filter(request: Request, name=None, loc=None, skills=None, status=None ,json_or_app="app",db: Session = Depends(get_db)):
	"""
	Display/GET all members or filtered members based on query params.
	
	- `/api/filter/json` return JSON response of all members or filtered
	- `/api/filter/app` retnders UI
	
	"""
	
	if json_or_app == "app":
		mmbr = db.query(Member)
		
		if name:
			mmbr = mmbr.filter(Member.full_name==name)
		if loc:
			mmbr = mmbr.filter(Member.cur_city==loc)
		# todo skills
		if status:
			mmbr = mmbr.filter(Member.cur_status==status)
		
	context = {
		"request": request,
		"members": mmbr,
		
		"name"   : name,
		"loc"    : loc,
		"status" : status
	}
	
	# template / json
	if json_or_app == "json":
		mmbr = db.query(Member).all()# filter secure key and other things that cause
		# security risk or optimisation probs
		return {"payload": mmbr}
	return templates.TemplateResponse("filter.html", context)



@app.post("/api/member")
def add_members(mmbr_req: MemberRequest, db: Session = Depends(get_db)):
	"""
	Adds new Member to database via API.
	Email must be unique
	"""
		
	mmbr = Member()
	# personal
	mmbr.full_name      = mmbr_req.full_name
	mmbr.nick_name      = mmbr_req.nick_name
	mmbr.cur_status     = mmbr_req.cur_status
	mmbr.cur_city       = mmbr_req.cur_city
	mmbr.bio            = mmbr_req.bio
	mmbr.communities    = mmbr_req.communities
	
	# social
	mmbr.twitter_url    = mmbr_req.twitter_url
	mmbr.github_url     = mmbr_req.github_url
	mmbr.linkedin_url   = mmbr_req.linkedin_url
	mmbr.whatsapp_num   = mmbr_req.whatsapp_num
	mmbr.email          = mmbr_req.email
	
	# skill
	mmbr.dom_1          = mmbr_req.dom_1
	mmbr.dom_2          = mmbr_req.dom_2
	mmbr.dom_3          = mmbr_req.dom_3
	mmbr.dom_4          = mmbr_req.dom_4
	mmbr.dom_5          = mmbr_req.dom_5
	mmbr.dom_5          = mmbr_req.dom_5
	mmbr.dom_6          = mmbr_req.dom_6
	mmbr.dom_7          = mmbr_req.dom_7
	mmbr.dom_8          = mmbr_req.dom_8
	mmbr.dom_1skill     = mmbr_req.dom_1skill
	mmbr.dom_1interest  = mmbr_req.dom_1interest
	mmbr.dom_2skill     = mmbr_req.dom_2skill
	mmbr.dom_2interest  = mmbr_req.dom_2interest
	mmbr.dom_3skill     = mmbr_req.dom_3skill
	mmbr.dom_3interest  = mmbr_req.dom_3interest
	mmbr.dom_4skill     = mmbr_req.dom_4skill
	mmbr.dom_4interest  = mmbr_req.dom_4interest
	mmbr.dom_5skill     = mmbr_req.dom_5skill
	mmbr.dom_5interest  = mmbr_req.dom_5interest
	mmbr.dom_6skill     = mmbr_req.dom_6skill
	mmbr.dom_6interest  = mmbr_req.dom_6interest
	mmbr.dom_7skill     = mmbr_req.dom_7skill
	mmbr.dom_7interest  = mmbr_req.dom_7interest
	mmbr.dom_8skill     = mmbr_req.dom_8skill
	mmbr.dom_8interest  = mmbr_req.dom_8interest
	
	mmbr.secret_key     = mmbr_req.secret_key
	
	dberror = None
	
	try: 
		db.add(mmbr)
		db.commit()
	except Exception as e:
		dberror = e
	# todo: catch sql integrity error: unique mail
	
	return {"status": "success/failed", "dberror": dberror}
	


@app.delete("/api/member")
def remove_members(mmbr_req: authMemberRequest, db: Session = Depends(get_db)):
	"""
	Remove entry wrt `secretkey` & **unique** `email` from database
	via API
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
	Alter values for an entry after verification via API
	"""
	
	secret_key = mmbr_req.secret_key
	email = mmbr_req.email
	mmbr = db.query(Member).filter(Member.secret_key==secret_key and Member.email==email).first()
	
	if mmbr is None:
		status = "secret key or email don't match"
	else:
		
		# take key where we need to update and value to 
		# which we have to update
		key       = mmbr_req.key
		val       = mmbr_req.val
		val_type  = mmbr_req.val_type # string by default "str"
		
		#mmbr.key = val (key is str)
		exec(f"mmbr.{key}={val_type}('{val}')") # field name from db must match exactly
		
		db.add(mmbr)
		db.commit()
		status = "success!"
		
	return {"status": status}
# ----------------------------------------
# end
# ----------------------------------------