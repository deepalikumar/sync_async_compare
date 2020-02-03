from flask import Blueprint
from flask_apispec import MethodResource, marshal_with

from .dal import get_user_posts
from .schemas import PostListSchema

blog = Blueprint("blog", __name__)


posts_list_schema = PostListSchema(many=True)


class UserResource(MethodResource):
    @marshal_with(posts_list_schema)
    def get(self, user_id):
        return get_user_posts(user_id)


blog.add_url_rule(
    "/users/<int:user_id>/posts/", view_func=UserResource.as_view("users_list")
)

