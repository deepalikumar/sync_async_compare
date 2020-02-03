from datetime import datetime

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    posts = db.relationship("Post", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"


class PostCategory(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), primary_key=True)

    post = db.relationship("Post", back_populates="categories")
    category = db.relationship("Category", back_populates="posts")

    def __repr__(self):
        return f"PostCategory(post_id={self.post_id}, category_id={self.category_id})"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    posts = db.relationship("PostCategory", back_populates="category")

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name})"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    category = db.relationship("PostCategory", back_populates="post")
    owner = db.relationship("User", uselist=False, back_populates="posts")

    def __repr__(self):
        return f"Post({self.id}, {self.title})"

