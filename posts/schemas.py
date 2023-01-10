from ninja import Schema

class PostCreateSchema(Schema):
    content: str
    hashtag: list

class PostUpdateSchema(Schema):
    content: str = None
    hashtag: list = None