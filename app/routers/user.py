

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter # import response and status from Fast API
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import engine, get_db

router= APIRouter(
    prefix = "/users",
    tags=['users']
) # create router object and replace app

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password
    hashed_password = utils.hash(user.password) # pass in the password
    user.password = hashed_password # update the pydantic user model with th ehashed password
 
    new_user = models.User(**user.model_dump()) ## This automatically unpacks the dictionary. No need for long form 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    #new_post = db.query(models.Post).

    #return{"data": new_post}
    return new_user


@router.get("/{id}", response_model=schemas.UserOut)  # << Decorator
def get_user(id: int, db: Session = Depends(get_db)): #Return User out Schema < Function parameters
    user = db.query(models.User).filter(models.User.id == id).first()


    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    return user