from pydantic import BaseModel, EmailStr, validator, StrictStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

##Just regular python classes
#class Post(BaseModel): # Class post that extends BaseModel
#    title: str
#    content: str
#    published: bool = True # default to true if user does not provide a value
#    #rating: Optional[int] = None # Fully optional field that defaults to value=None ( Note you need to import Optional from typing)

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass # Extend fully


class UserOut(BaseModel): #Define response model without password
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True #converts response to dictionary for ORM Models like pydantic

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut # to work with relationship.


    class Config:
        from_attributes = True #converts response to dictionary for ORM Models like pydantic


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True #converts response to dictionary for ORM Models like pydantic

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Define a schema for the token ( For anythign expected from user)

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) #allow zeros and ones only