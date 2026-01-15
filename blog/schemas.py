from pydantic import BaseModel
from typing import List, Optional

class Blog(BaseModel):
    title: str
    body: str
    user_id: int


class BlogCreate(Blog):
    pass


class ShowBlog(BaseModel):
    id:int
    title: str
    body: str
    creator: Optional["User"] = None

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str


class UserCreate(User):
    password: str


class ShowUser(User):
    id: int
    blogs: List[ShowBlog] = []

    class Config:
        orm_mode = True

