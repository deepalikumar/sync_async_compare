from flask_apispec import MethodResource

from .dal import get_user_posts


class PostListResource(MethodResource):
    def get(self):
        pass
