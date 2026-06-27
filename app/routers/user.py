from fastapi import FastAPI , Response , status , HTTPException, Depends , APIRouter
from sqlalchemy.orm import Session
from ..import models , schemas , utilis
from ..database import  get_db


# using router : helps to split up the crud code into multiple files used inplace of app in main apimaking file 
router=APIRouter(
    prefix="/users",
    tags=['Users']
)

# ******Making user system*******


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserCreateSend)
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):

    #hash the password - user.password
    hashed_password  = utilis.hash(user.password)
    user.password=hashed_password
    
    
    new_user= models.User(**user.dict())  
    db.add(new_user)  
    db.commit()  
    db.refresh(new_user)
    
    return new_user


@router.get('/{id}',response_model=schemas.UserCreateSend)
def get_user(id:int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    return user
