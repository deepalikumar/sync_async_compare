import asyncio
from itertools import groupby

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .tables import Post, User, Comment, Category, PostCategory
from .models import Post as PostModel


async def get_user_posts(user_id, *, category_id=None, limit=10, offset=0):
    from resources import database

    limit = limit if 1 <= limit <= 50 else 10
    offset = offset if offset >= 0 else 0
    post_query = (
        Post.select().where(Post.c.owner_id == user_id).limit(limit).offset(offset)
    )
    if category_id:
        post_query = post_query.where(Post.c.category_id == category_id)

    posts = await database.fetch_all(post_query)

    post_ids = [post["id"] for post in posts]
    comments, categories, owner = await asyncio.gather(
        database.fetch_all(Comment.select().where(Comment.c.post_id.in_(post_ids))),
        database.fetch_all(
            select([PostCategory.c.post_id, Category.c.id, Category.c.name]).where(
                PostCategory.c.post_id.in_(post_ids)
            )
        ),
        database.fetch_one(User.select().where(User.c.id == user_id)),
    )

    grouped_comments = {
        post_id: list(post_comments)
        for post_id, post_comments in groupby(
            comments, lambda comment: comment["post_id"]
        )
    }
    grouped_categories = {
        post_id: list(post_categories)
        for post_id, post_categories in groupby(
            categories, lambda category: category["post_id"]
        )
    }

    results = []
    for post in posts:
        res = dict(post)
        res["owner"] = owner
        res["comments"] = grouped_comments.get(res["id"], [])
        res["categories"] = grouped_categories.get(res["id"], [])

        results.append(res)

    return results


def get_user_posts_sync(session, user_id, *, category_id=None, limit=10, offset=0):
    user_posts = session.query(PostModel).filter(PostModel.owner_id == user_id)
    if category_id:
        user_posts = user_posts.filter(PostModel.category_id == category_id)
    limit = limit if 1 <= limit <= 50 else 10
    offset = offset if offset >= 0 else 0
    return (
        user_posts.options(selectinload(PostModel.comments))
        .options(selectinload(PostModel.owner))
        .options(selectinload(PostModel.categories))
        .offset(offset)
        .limit(limit)
        .all()
    )
