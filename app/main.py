from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

#print(settings)

# models.Base.metadata.create_all(bind=engine)
# replaced by Alembic


#create instance of FastAPI
app = FastAPI()


# can allow specific domains and specific requests such as get only.
origins = [
    "http://www.google.com",
    "http://localhost"

]

#origins = ["*"]

app.add_middleware( # runs before our application
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(post.router) # First hit of an app
app.include_router(user.router) # second hit of an app
app.include_router(auth.router) 
app.include_router(vote.router)

#Path operation or Route
@app.get("/")                           # Decorator - This turns htis into an path operator to the endpoint is usable e.b. a get method plus path
async def root():                       # Function - async is optional but required when asynchronous task (takes time) name of the function here is root but it can be anything. root is default
    return {"message": "Welcome to my API"}



##----------------------Old-------------------------------

#from fastapi import FastAPI #, Response, status, HTTPException, Depends # import response and status from Fast API
#from fastapi.params import Body
#from pydantic import BaseModel
#
#from random import randrange
#from sqlalchemy.orm import Session
#from . import models#, schemas, utils, oauth2
#from .database import engine #, get_db
#from.routers import post, user, auth

#
#models.Base.metadata.create_all(bind=engine)


#create instance of FastAPI
#app = FastAPI()

#using pydantic to define the schema
# title str, content str can extend to , category
# cretae  anew class and make it extend BaseModel


#Connection to database
#as this can fail, use 'try'. Used for any command that could fail



#Create a variable to store posts
#create an array/dictionary
#my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favourite foods", "content": "I like pizza", "id": 2}] # hardcoded 

#def find_post(id): # define simple function to retrieve post NOT BEST PRACTICE
#    for p in my_posts:
#        if p["id"] == id:
#            return p
#
#def find_index_post(id): # retrieve index of post
#    for i,p in enumerate(my_posts): # enumerate and look through array (my_posts)
#        if p['id'] == id:
#            return i



#app.include_router(post.router) # First hit of an app
#app.include_router(user.router) # second hit of an app
#app.include_router(auth.router) # First hit of an app

#Path operation or Route
#@app.get("/")                           # Decorator - This turns htis into an path operator to the endpoint is usable e.b. a get method plus path
#async def root():                       # Function - async is optional but required when asynchronous task (takes time) name of the function here is root but it can be anything. root is default
#    return {"message": "Welcome to my API"}


####Dont need this with schemas 
####@app.get("/sqlalchemy")
####def test_posts(db: Session = Depends(get_db)): # Passing in DB session objects. 
####  
####    posts = db.query(models.Post).all() # Grab all entries in the poet table # Gets all data without using SQL.
####    #this creates the query db.query(models.Post)
####    #this runs the query .all()
####
####    print(posts)
####    return {"data": posts}



