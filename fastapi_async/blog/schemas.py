from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True


class Category(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Comment(BaseModel):
    id: int
    commenter: str
    comment: str
    post_id: Optional[str]

    class Config:
        orm_mode = True


class Post(BaseModel):
    id: int
    title: str
    body: str
    pub_date: datetime
    owner: User
    comments: List[Comment] = []
    categories: List[Category]

    class Config:
        orm_mode = True
