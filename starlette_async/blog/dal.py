import asyncio
from itertools import groupby

from sqlalchemy import select

from app import database
from .tables import post, user, comment, category, post_category


async def get_user_posts(user_id, *, category_id=None, limit=10, offset=0):
    limit = limit if 1 <= limit <= 50 else 10
    offset = offset if offset >= 0 else 0
    post_query = (
        post.select().where(post.c.owner_id == user_id).limit(limit).offset(offset)
    )
    if category_id:
        post_query = post_query.where(post.c.category_id == category_id)

    posts = await database.fetch_all(post_query)

    post_ids = [p["id"] for p in posts]
    comments, categories, owner = await asyncio.gather(
        database.fetch_all(comment.select().where(comment.c.post_id.in_(post_ids))),
        database.fetch_all(
            select([post_category.c.post_id, category.c.id, category.c.name]).where(
                post_category.c.post_id.in_(post_ids)
            )
        ),
        database.fetch_one(user.select().where(user.c.id == user_id)),
    )

    grouped_comments = {
        post_id: list(post_comments)
        for post_id, post_comments in groupby(comments, lambda x: x["post_id"])
    }
    grouped_categories = {
        post_id: list(post_categories)
        for post_id, post_categories in groupby(categories, lambda x: x["post_id"])
    }

    results = []
    for p in posts:
        res = dict(p)
        res["owner"] = owner
        res["comments"] = grouped_comments.get(res["id"], [])
        res["categories"] = grouped_categories.get(res["id"], [])

        results.append(res)

    return results
