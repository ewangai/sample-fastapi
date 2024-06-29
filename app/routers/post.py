from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter # import response and status from Fast API
from fastapi.params import Body
from pydantic import BaseModel
from typing import List, Optional #List for schema model
from random import randrange
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy import func, desc 
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import engine, get_db
#from  oauth2 import get_current_user

#when working wiht routers you can pass parameters into route
router= APIRouter(
    prefix="/posts",
    tags=['posts']
) # create router object and replace app

#@router.get("/")                      # use get to retrieve data
@router.get("/", response_model=List[schemas.PostOut])                      # use get to retrieve data
#async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = "*"): #Search for titles wiht at least one space
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 100, skip: int = 0): #Search for titles wiht at least one space
    #return {"data": "This is your post"}
    #get posts form DB
    ##Direct method cursor.execute("""SELECT * FROM posts""")
    ##Direct method posts=cursor.fetchall() #use fetchone for ID search as it exits when found
    #print(posts) # return from DB - To console

    #posts = db.query(models.Post).all() # ORM method - retrieve all posts
    #old#posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).order_by(desc(models.Post.id)).limit(limit).offset(skip).all() #how to join with SQL Alchemy


    #posts = db.query(models.Post).filter( models.Post.owner_id == current_user.id) # get jjst the current user postsORM method

    #return {"data": posts} # Fast API has a automatic serializer that converts this into JSON
    #return  posts # Fast API has a automatic serializer that converts this into JSON
    posts = list ( map (lambda x : x._mapping, posts) )
    return(posts)




#before using pydantic
#@app.post("/createposts")
#def create_posts(payLoad: dict = Body(...)): # converting body into a python dictionary then saving it into a payLoad variable
#    print(payLoad)
#    #return {"message": "successfully created post"}
#    return {"new_post": f"title: {payLoad['title']} content: {payLoad['content']}"}

#Commentend to retain first pydantic usage
#with pydantic to defie schema
#@app.post("/createposts")
#def create_posts(post: Post): # using pydantic schema to define inputs and validate
#    print(post) # prints all in console                 e.g title='Top beaches in Florida' content='Check out these awesome beaches' published=True rating=4
#    print(post.dict()) # This sends it out as a dict.   e.g {'title': 'Top beaches in Florida', 'content': 'Check out these awesome beaches', 'published': True, 'rating': 4}
#    return {"data" : "new_post"}

#onto CRUD
#with pydantic to defie schema
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # add a 201 stattus when created
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # using pydantic schema to define inputs and validate 







    #print(post) # prints all in console                 e.g title='Top beaches in Florida' content='Check out these awesome beaches' published=True rating=4
    #print(post.dict()) # This sends it out as a dict.   e.g {'title': 'Top beaches in Florida', 'content': 'Check out these awesome beaches', 'published': True, 'rating': 4}
    #post_dict = post.dict()
    #post_dict['id'] = randrange(0,99999999999) #adds to ID with a random number 
    #post_dict['title'] = "Favourite country" #adds to ID with a random number 
    #my_posts.append(post_dict)
    
    #Use DB
    ##Direct method cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """
    ##Direct method                ,(post.title, post.content, post.published)) #Parameterise to avoid SQL injection
   ##Direct method new_post = cursor.fetchone()
    #remember to commit in postgress and oracle]
    
    #
    #print(current_user.id)
    #print(**post.model_dump())
    #new_post = models.Post(title=post.title, content=post.content, published=post.published) # Long form unpack
    new_post = models.Post(owner_id=current_user.id,**post.model_dump()) ## This automatically unpacks the dictionary. No need for long form 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    #new_post = db.query(models.Post).
    #print(user_id)
    #return{"data": new_post}
    return new_post



@router.get("/{id}", response_model=schemas.PostOut) #ID will be passed in and embeded in the URL as a path parameter.
#def get_post(id):
#def get_post(id: int, response: Response): # this uses fast API to convert the value to an integer
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # this uses fast API to convert the value to an integer

    #Direct DB # cursor.execute("""SELECT * FROM posts WHERE id = %s """,str(id))
    #Direct DB # post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first() # Where clause equivalent
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    #print(id) # vanilla get for specific ID
    #post = find_post(id) #this will use the function defined earlier to search for the ID # not earlier conversion, no need to int here
    #post = find_post(int(id)) #this will use the function defined earlier to search for the ID # Note conversion to integer
    #return {"post_detail": f"Here is post {id}"} # vanilla get for specific ID without function
    
    if not post:
        #response.status_code = 404 # override the response from a 200 to a 404
        #response.status_code = status.HTTP_404_NOT_FOUND # override the response from a 200 to a 404 with the status method. ** Not needed with HTTP Exception
        #return {'message': f"post with id: {id} was not found"} # considered sloopy but works. Requires hardcoding  ** Not needed with HTTP Exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found") # cleaner and it just needs the code and message in one line.
    #return {"post_detail": post }
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) # delete HTTP request for the decorator
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # define the function
    
     #Direct DB # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",str(id))
    #Direct DB # deleted_post = cursor.fetchone()
    #Direct DB # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)#.first() # Where clause equivalent

    post = post_query.first()    

    #print(current_user.id)

    #deleting post
    # find index in the array that has required ID
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
        

    post_query.delete(synchronize_session=False)
    db.commit()


    #return{'message': "post was successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT) # 204 when you delete sometning in FastAPI no data goes back.

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
 
    #Direct DB # cursor.execute("""UPDATE posts set title = %s, content = %s,  published = %s WHERE id = %s returning *""", (post.title, post.content, post.published,str(id)))
    #Direct DB # updated_post = cursor.fetchone()
    #Direct DB # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    #index = find_index_post(id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
        

    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()

    #post_dict = post.dict() #take all data and convert into a python dis=ctionary
    #post_dict['id'] = id # add the id so it has ID 
    #my_posts[index] = post_dict # replace spot in array wth new disct
    #return {'data': post_dict}
    #return {"data": post_query.first()} # indlucing data Keyword in JSON
    return post_query.first()


