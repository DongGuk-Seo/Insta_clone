from ninja import Schema
from post.models import (
    PostModel, 
    PostImageModel, 
    PostHashtagModel,
    )

class PostCreate(Schema):
    content: str
    hashtag: list

class PostUpdate(Schema):
    content: str = None
    hashtag: list = None