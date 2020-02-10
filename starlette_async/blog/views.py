from starlette.responses import UJSONResponse
from starlette.endpoints import HTTPEndpoint
from starlette.routing import Route
from spectree import Response

from app import api
from .dal import get_user_posts
from .schemas import PostListSchema


class UserPostListEndpoint(HTTPEndpoint):
    async def get(self, request):
        user_id = request.path_params["user_id"]
        return UJSONResponse(await get_user_posts(user_id))
