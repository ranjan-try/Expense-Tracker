from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import Base,engine, get_db
from app import models,schemas


Base.metadata.create_all(bind=engine)
app = FastAPI()


#creating users.

@app.get("/users/count")
def count_users(db: Session = Depends(get_db)):     #depend here is for dependency injection like it tells that before running the function run the function inside it and pass it in the parameter
   count = db.query(models.User).count()
   return {"count": count} 

@app.get("/users/{user_id}",response_model=schemas.UserResponse)
def get_user(user_id: int,db: Session = Depends(get_db)):
    # #getting user from the database using the general method to get row from a database
    # user = db.query(models.User).filter(models.User.id == user_id).first()    
    # getting user from the database using the standard method to get row from a database using id.
    user = db.get(models.User,user_id)
    if user is None:
        raise HTTPException(status_code=404,detail="User not Found!!")

    return user


@app.post("/users",response_model=schemas.UserResponse)
def create_user(user_inp: schemas.UserCreate,db: Session = Depends(get_db)):

    existing = db.query(models.User).filter(models.User.email == user_inp.email).first()  #SELECT * FROM User WHERE email = "" LIMIT 1;
    if existing:
        raise HTTPException(status_code=409, detail="email already in use")

    user = models.User(name=user_inp.name,email=user_inp.email,password_hash="RAj") #object of the User 

    db.add(user)
    db.commit()
    db.refresh(user)
    return user# response model manage to convert . into json


#creating categories...

@app.post("/categories",response_model=schemas.CategoryResponse)

def create_category(category_in: schemas.CategoryCreate,db: Session = Depends(get_db)):
    user = db.get(models.User,category_in.user_id)
    if user is None:
        raise HTTPException(status_code=404,detail="User id not Found")

    existing = db.query(models.Category).filter(models.Category.user_id == category_in.user_id, models.Category.name == category_in.name).first()
    if existing:
        raise HTTPException(status_code=409,detail="category already exists")
    category = models.Category(name=category_in.name,type=category_in.type,user_id=category_in.user_id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
