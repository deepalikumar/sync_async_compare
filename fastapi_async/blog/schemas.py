from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str


class Category(BaseModel):
    id: int
    name: str


class Comment(BaseModel):
    id: int
    commenter: str
    comment: str
    post_id: Optional[str]


class Post(BaseModel):
    id: int
    title: str
    body: str
    pub_date: datetime
    owner: User
    comments: List[Comment] = []
    categories: List[Category]
