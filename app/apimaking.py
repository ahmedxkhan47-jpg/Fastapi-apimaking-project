from fastapi import FastAPI , Depends
# from fastapi.params import Body
from fastapi.middleware.cors import CORSMiddleware

# from typing import Optional , List

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
#from sqlalchemy.orm import Session
from .import models 
from .database import engine , get_db
from .routers import post,user,auth,vote


# models.Base.metadata.create_all(bind=engine) makes sqlalchemy create add querys


app = FastAPI()

origins=["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"message": "kia haal ha bhai theak hoa na khariat ha"}



    
# hardcoded data    
# my_posts = [{"title" : "title of post 1", "content" : "content of post 1", "id" : 1} , {"title" :
#     "favourite food", "content" : "I like pizza", "id" : 2}]


# def find_post(id):
#     for p in my_posts:
#       if p["id"]==id:
#           return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#       if p ['id']==id:
#           return i




# os code

# import os 
# path=os.getnv("MY_DB_URL")
# print(path)







