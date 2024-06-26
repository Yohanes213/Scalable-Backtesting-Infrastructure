from typing import Optional
from pydantic import BaseModel



class UserCreate(BaseModel):     
    username: str
    password: str

class UserInDB(UserCreate):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserResponse(BaseModel):
    user_id  : int
    username: str
    


class Config:
        orm_mode = True