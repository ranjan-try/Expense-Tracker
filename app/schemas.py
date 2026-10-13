from pydantic import BaseModel, ConfigDict
from typing import Literal

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
    
    