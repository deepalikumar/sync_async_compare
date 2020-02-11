from typing import List

from fastapi import APIRouter, Depends

from resources import get_session
from .dal import get_user_posts, get_user_posts_sync
from .schemas import PostSchema, PostORMSchema


async def user_posts(user_id: int):
    posts = await get_user_posts(user_id)
    return posts


def user_posts_sync(user_id: int, session=Depends(get_session)):
    posts = get_user_posts_sync(session, user_id)
    return posts


router = APIRouter()
router.add_api_route(
    "/users/{user_id}/posts",
    user_posts,
    response_model=List[PostSchema],
    methods=("GET",),
)
router.add_api_route(
    "/users/{user_id}/posts/sync",
    user_posts_sync,
    response_model=List[PostORMSchema],
    methods=("GET",),
)
