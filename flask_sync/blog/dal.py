from sqlalchemy.orm import joinedload
from .models import Post, User


def get_user_posts(user_id, *, category_id=None, limit=10, offset=0):
    user_posts = Post.query.filter(Post.owner_id == user_id)
    if category_id:
        user_posts = user_posts.filter(Post.category_id == category_id)
    limit = limit if 1 <= limit <= 50 else 10
    offset = offset if offset >= 0 else 0
    return (
        user_posts.options(joinedload(Post.comments))
        .options(joinedload(Post.owner))
        .options(joinedload(Post.categories))
        .offset(offset)
        .limit(limit)
    )
