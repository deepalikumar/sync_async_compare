from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Text, DateTime
from app import metadata


User = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(80), unique=True, nullable=False),
    Column("email", String(120), unique=True, nullable=False),
)


Category = Table(
    "category",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), unique=True, nullable=False),
)


Post = Table(
    "post",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(80), nullable=False),
    Column("body", Text, nullable=False),
    Column("pub_date", DateTime, nullable=False, default=datetime.utcnow),
    Column(
        "owner_id", Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False
    ),
)


PostCategory = Table(
    "post_category",
    metadata,
    Column(
        "post_id", Integer, ForeignKey("post.id", ondelete="cascade"), primary_key=True
    ),
    Column(
        "category_id",
        Integer,
        ForeignKey("category.id", ondelete="cascade"),
        primary_key=True,
    ),
)


Comment = Table(
    "comment",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("commenter", String(80), nullable=False),
    Column("comment", Text, nullable=False),
    Column(
        "post_id", Integer, ForeignKey("post.id", ondelete="cascade"), nullable=False
    ),
)
