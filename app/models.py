from app.database import Base 
from sqlalchemy import INTEGER,String,Column,ForeignKey,Numeric,Date
from datetime import date


class User(Base):
    __tablename__ = "users"
    id = Column(INTEGER,primary_key=True)
    name = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    password_hash = Column(String,nullable=False)




class Category(Base):
    __tablename__ = "categories"
    id = Column(INTEGER,primary_key=True)
    name = Column(String,nullable=False)
    type = Column(String,nullable=False)
    user_id = Column(INTEGER,ForeignKey("users.id"),nullable=False)





class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(INTEGER,primary_key=True)
    user_id = Column(INTEGER,ForeignKey("users.id"),nullable=False)
    amount = Column(Numeric(10,2),nullable=False)
    type = Column(String,nullable=False)
    description = Column(String)
    category_id= Column(INTEGER,ForeignKey("categories.id"),nullable=False)
    date = Column(Date,default=date.today)



#Numeric is for storing floating numbers to a precision 
class Budget(Base):
    __tablename__ = "budgets"
    id = Column(INTEGER,primary_key=True)
    user_id = Column(INTEGER,ForeignKey("users.id"),nullable=False)
    category_id= Column(INTEGER,ForeignKey("categories.id"),nullable=False)
    limit_amount = Column(Numeric(10,2),nullable=False)
    month = Column(INTEGER,nullable=False)
    year = Column(INTEGER,nullable=False)

