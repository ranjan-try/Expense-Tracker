from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
from decimal import Decimal
import datetime


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    model_config = ConfigDict(from_attributes=True)   
    #This will make sure that it doesnt need just json and can get data directly from the database

class CategoryCreate(BaseModel):
    name: str
    type: Literal["income","expense"]
    user_id: int

class CategoryResponse(CategoryCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class TransactionCreate(BaseModel):
    user_id: int
    category_id: int
    type: Literal["income","expense"]
    description: str | None = None
    amount: Decimal = Field(gt=0)
    date : datetime.date | None = None
    
class TransactionResponse(TransactionCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
    