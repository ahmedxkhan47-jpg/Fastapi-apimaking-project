
from fastapi import FastAPI , Response , status , HTTPException, Depends , APIRouter
from sqlalchemy.orm import Session
from ..import models , schemas ,oauth2
from ..database import  get_db
from typing import  List , Optional
from sqlalchemy import func

 # using router : helps to split up the crud code into multiple files used inplace of app in main apimaking file 
router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)




# GETIING POST WITH SQLALCHEMY
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db)  , current_user:int=Depends(oauth2.get_current_user),limit:int = 10
              ,skip:int =0,search:Optional[str]=" "):
  print(limit)
    # to get only valid get.filter(models.Post.owner_id==current_user.id).all()
  
  post=db.query(models.Post,func.count(models.vote.post_id).label("votes")).join(models.vote,models.Post.id==models.vote.post_id, 
  isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  
  return post



# POSTING POST WITH SQLALCHEMY
@router.post("/", status_code=status.HTTP_201_CREATED , response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db) 
                 , current_user:int=Depends(oauth2.get_current_user)): 

   

   # inefficent way new_post1=models.Post(title=post.title,content=post.content,published=post.published)
   
   
    
    
    # owner_id =current_user.id is very important so we can take the id of the user as it is not send by him
    #efficent way
    new_post1= models.Post(owner_id=current_user.id ,**post.dict())  # ** unpaking dictinary
    
    
    db.add(new_post1)  
    db.commit()  # commit change in databse
    db.refresh(new_post1) # retriving post we made and store in new_post1
    
    return  new_post1 


# getting post by id with SQL ALCHEMY
@router.get("/{id}", response_model=schemas.PostOut)
def get_posts(id:int, db:Session = Depends(get_db) , current_user:int=Depends(oauth2.get_current_user)):
     
    #  posts=db.query(models.Post).filter(models.Post.id==id).first()
     
    # normal way post=find_post(id)
    
     posts=db.query(models.Post,func.count(models.vote.post_id).label("votes")).join(models.vote,models.Post.id==models.vote.post_id, 
  isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    
     if not posts:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
     
    #  if posts.owner_id != current_user.id:  if need only person that post  see his post
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                        detail=f"Not Authorized to perform requested action")
     
     
     return  posts


# deleting post with SQL ALchemy
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int, db:Session = Depends(get_db) , current_user:int=Depends(oauth2.get_current_user)):
    
  
     post_querry = db.query(models.Post).filter(models.Post.id==id)
    
     post=post_querry.first()
    
     if post == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} does not exist")
    
     if post.owner_id != current_user.id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                           detail=f"Not Authorized to perform requested action")
    
    
    # real deleting happening
     post_querry.delete(synchronize_session=False) 
     db.commit()
     
     return Response(status_code=status.HTTP_204_NO_CONTENT)


# Updating Post with SQL ALCHEMY
@router.put("/{id}", response_model=schemas.Post)
def update_posts(id:int, updated_post:schemas.PostCreate, db:Session = Depends(get_db) 
                 , current_user:int=Depends(oauth2.get_current_user)):   
    
     post_query = db.query(models.Post).filter(models.Post.id==id)
     post = post_query.first() # to run the querry
     
    
     if post is None:  # check if id is present
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} does not exist")
 
   
     if post.owner_id != current_user.id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                           detail=f"Not Authorized to perform requested action")
    
    
    #  post_query.update({'title' : 'hey this is my updated title' ,
    #                    'content':'this is my updated content'}, synchronize_session=False)   if present update it
    
     post_query.update(updated_post.dict(),synchronize_session=False)
     
     db.commit()
     
     return post_query.first()
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
# # ****** RAW SQL CODE  ******


# # GETTING POST WITH RAW SQL
# @router.get("/posts", response_model=schemas.Post)
# def get_posts():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     print(posts)
#     return{"data":posts}



# #posting post with RAW SQL
# @router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_posts(new_post:schemas.PostCreate):
#     # post_dict = new_post.dict()
#     # post_dict['id']= randrange(0,1000000)
#     # my_posts.append(post_dict)
    
#     #sql injection
#     cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING* """,(new_post.title,
#                                                                                           new_post.content,
#                                                                                           new_post.published))
#     new_post1=cursor.fetchone()
    
#     #push changes in database 
#     conn.commit() 
    
#     return  new_post1


# # getting post by id with RAW SQL
# @router.get("/posts/{id}", response_model=schemas.Post)
# def get_post(id:int):
    
#     # normal way post=find_post(id)
#     cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id),))  #iteratable appraoch kuch ha so ,
#     post=cursor.fetchone()
#     if not post:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
#     return {"post_detail" : post}


# # deleting post with RAW SQL
# @router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
    
#     cursor.execute("""DELETE FROM posts WHERE id=%s returning *""", (str(id))) # statment
#     deleted_post=cursor.fetchone() # execute sql statment
#     conn.commit() # commit change in database
    
    
#     # index=find_index_post(id)
    
#     if deleted_post is None:
#      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} does not exist")
    
#     #my_posts.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# # Updating Post with Raw SQL
# @router.put("/posts/{id}", response_model=schemas.Post)
# def update_post(id:int,post:schemas.PostCreate):
    
#     cursor.execute("""UPDATE posts SET title=%s, content=%s , published=%s WHERE id=%s RETURNING *""" , 
#                    (post.title,post.content,post.published,str(id)))
#     updated_post=cursor.fetchone()
#     conn.commit()
#     #index=find_index_post(id)
    
#     if updated_post is None:
#      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} does not exist")
 
#     # post_dict=post.dict()
#     # post_dict['id']=id
#     # my_posts[index]=post_dict
#     return updated_post
# # @app.get("/items/{item_id}")
# # def read_item(item_id: int, q: str | None = None):
# #     return {"item_id": item_id, "q": q}


