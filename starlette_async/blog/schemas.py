from typing import List
from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    email: str


class CategorySchema(BaseModel):
    id: int
    name: str


class CommentSchema(BaseModel):
    id: int
    commenter: str
    comment: str


class PostSchema(BaseModel):
    id: int
    title: str
    body: str
    comments: List[CommentSchema] = []
    categories: List[CategorySchema]
