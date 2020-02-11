from typing import List

from fastapi import APIRouter, Depends

from resources import get_session
from .dal import get_user_posts, get_user_posts_sync
from .schemas import Post

router = APIRouter()


@router.get("/users/{user_id}/posts", response_model=List[Post])
async def user_posts(user_id: int):
    posts = await get_user_posts(user_id)
    return posts


@router.get("/users/{user_id}/posts/sync", response_model=List[Post])
def user_posts_sync(user_id: int, session=Depends(get_session)):
    posts = get_user_posts_sync(session, user_id)
    return posts
