from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    commenter = fields.Str(required=True)
    comment = fields.Str(required=True)


class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    body = fields.Str(required=True)
    pub_date = fields.DateTime(required=True)


class PostListSchema(PostSchema):
    categories = fields.Nested(CategorySchema, many=True, dump_only=True)
    owner = fields.Nested(UserSchema, dump_only=True)
    comments = fields.Nested(CommentSchema, many=True, dump_only=True)
