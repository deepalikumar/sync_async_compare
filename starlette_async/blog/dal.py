from sqlalchemy import select

from app import database
from .tables import post, user, comment, category, post_category


async def get_user_posts(user_id, *, category_id=None, limit=10, offset=0):
    joined = (
        post.join(comment)
        .join(user, post.c.owner_id == user.c.id)
        .join(post_category)
        .join(category, category.c.id == post_category.c.category_id)
    )
    query = (
        select([post, category, comment, user])
        .where(post.c.owner_id == user_id)
        .select_from(joined)
    )
    if category_id:
        query = query.where(post.c.category_id == category_id)
    limit = limit if 1 <= limit <= 50 else 10
    offset = offset if offset >= 0 else 0
    query = query.limit(limit).offset(offset)
    print(query)
    return await database.fetch_all(query)
