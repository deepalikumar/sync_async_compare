from starlette.responses import UJSONResponse
from starlette.endpoints import HTTPEndpoint
from starlette.routing import Route


class UserListEndpoint(HTTPEndpoint):
    async def get(self, request):
        return UJSONResponse({"hello": "world"})
