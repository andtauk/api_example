from pydantic import BaseModel, EmailStr
from datetime import datetime

##usuário servidor
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

#servidor usuário

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut (BaseModel):
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
