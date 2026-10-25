from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import Base,engine, get_db
from app import models,schemas
from typing import Literal
from datetime import date
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
    return user # response model manage to convert . into json


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

#creating the transaction 

@app.post("/transactions",response_model=schemas.TransactionResponse)
def create_transaction(transaction_in: schemas.TransactionCreate, db: Session = Depends(get_db)):
    user = db.get(models.User,transaction_in.user_id)
    if user is None:
        raise HTTPException(status_code=404,detail="user not found")
    category = db.query(models.Category).filter(models.Category.id == transaction_in.category_id).first()
    if category is None:
        raise HTTPException(status_code=404,detail="Category not FOUND")
    #checking if category matches to the user 
    if(category.user_id != user.id):
        raise HTTPException(status_code=403,detail="Category doesn't belong to the User")

    if(category.type != transaction_in.type):
        raise HTTPException(status_code=400,detail="type Not match Error")
    
    transaction = models.Transaction(user_id = transaction_in.user_id,amount = transaction_in.amount,type = transaction_in.type,description = transaction_in.description,category_id = transaction_in.category_id,date = transaction_in.date)
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

@app.get("/transactions",response_model=list[schemas.TransactionResponse])
def get_transaction(user_id:int,category_id:int | None = None,start_date: date | None = None,end_date: date | None = None,type: Literal["income","expense"] | None=None,db: Session = Depends(get_db)):
    user = db.get(models.User,user_id)
    if user is None:
        raise HTTPException(status_code=404,detail="user not FOUND")
    transaction = db.query(models.Transaction).filter(models.Transaction.user_id == user_id)
    if type is not None:
        transaction = transaction.filter(models.Transaction.type == type)  
    
    if category_id is not None:
        transaction = transaction.filter(models.Transaction.category_id == category_id)

    #date filter
    if start_date and end_date and start_date > end_date:
        raise HTTPException(status_code=400,detail="start_date cant be after end_date")
    if start_date is not None:
        transaction = transaction.filter(models.Transaction.date >= start_date)
    if end_date is not None:
        transaction = transaction.filter(models.Transaction.date <= end_date)
    transaction = transaction.order_by(models.Transaction.date.desc())
    
    return transaction.all()

@app.delete("/transactions/{transaction_id}",status_code=204)
def delete_transaction(transaction_id: int,db: Session = Depends(get_db)):
    transaction = db.get(models.Transaction,transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404,detail="transaction_id not found")

    db.delete(transaction)
    db.commit()


    







