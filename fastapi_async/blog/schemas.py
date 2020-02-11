from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    email: str


class UserORMSchema(UserSchema):
    class Config:
        orm_mode = True


class CategorySchema(BaseModel):
    id: int
    name: str


class CategoryORMSchema(CategorySchema):
    class Config:
        orm_mode = True


class CommentSchema(BaseModel):
    id: int
    commenter: str
    comment: str


class CommentORMSchema(CommentSchema):
    class Config:
        orm_mode = True


class PostSchema(BaseModel):
    id: int
    title: str
    body: str
    pub_date: datetime
    owner: UserSchema
    comments: List[CommentSchema] = []
    categories: List[CategorySchema]


class PostORMSchema(PostSchema):
    owner = UserORMSchema
    comments: List[CommentORMSchema] = []
    categories: List[CategorySchema]

    class Config:
        orm_mode = True
