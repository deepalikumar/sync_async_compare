from typing import List

from fastapi import APIRouter

from .dal import get_user_posts
from .schemas import Post

router = APIRouter()


@router.get("/users/{user_id}/posts", response_model=List[Post])
async def user_posts(user_id: int):
    posts = await get_user_posts(user_id)
    return posts
