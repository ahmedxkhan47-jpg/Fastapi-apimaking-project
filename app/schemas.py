
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint
# schhema
# class Post(BaseModel):
#     title:str
#     content: str
#     published : bool = True  # like this can give value or not
   # rating: Optional[int] = None 
   
 # schema  
   
class PostBase(BaseModel):
    title:str
    content: str
    published : bool = True 

class PostCreate(PostBase): # inheritance from postbase
    pass  # just accept from postbase


class UserCreateSend(BaseModel):
    id:int
    email:EmailStr
    class Config:
       from_attributes=True 

    
          
class Post(PostBase):
    id:int
    # title: str
    # content:str         inherting the three from PostBase
    # published:bool
    created_at:datetime  
    owner_id:int
    owner:UserCreateSend        
    # to convert from sqlAlchemy model to pydantic model ignoring it is not a dictionary
    class Config:
        from_attributes=True   # form_attributes is new way but can also use orm_model
        
class PostOut(BaseModel):
    Post:Post
    votes:int
    
    class Config:
        from_attributes=True
        
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
            
            
class UserLogin(BaseModel):
     email: EmailStr
     password: str
     
class Token(BaseModel):
    access_token:str
    token_type:str     
    
class TokenData(BaseModel):
    id: Optional[int]=None    
    
    
class vote(BaseModel):
    post_id:int
    dir:conint(le=1)     # type: ignore    // o or 1 suppose here in le=1
    
    
    