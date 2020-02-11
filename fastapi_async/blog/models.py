from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from resources import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)

    posts = relationship("Post", back_populates="owner")

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"


class PostCategory(Base):
    __tablename__ = "post_category"

    post_id = Column(Integer, ForeignKey("post.id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("category.id"), primary_key=True)

    post = relationship("Post", back_populates="post_categories")
    category = relationship("Category", back_populates="post_categories")

    def __repr__(self):
        return f"PostCategory(post_id={self.post_id}, category_id={self.category_id})"


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    post_categories = relationship("PostCategory", back_populates="category")
    posts = relationship(
        "Post", secondary=PostCategory.__table__, back_populates="categories"
    )

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name})"


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    body = Column(Text, nullable=False)
    pub_date = Column(DateTime, nullable=False, default=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    post_categories = relationship("PostCategory", back_populates="post")
    categories = relationship(
        "Category", secondary=PostCategory.__table__, back_populates="posts"
    )
    owner = relationship("User", uselist=False, back_populates="posts")
    comments = relationship("Comment", back_populates="post")

    def __repr__(self):
        return f"Post({self.id}, {self.title})"


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    commenter = Column(String(80), nullable=False)
    comment = Column(Text, nullable=False)

    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)

    post = relationship("Post", uselist=False, back_populates="comments")
