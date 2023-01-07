from ninja import Schema
from post.models import (
    PostModel, 
    PostImageModel, 
    PostHashtagModel,
    PostCommentModel,
    PostCommentReplyModel
    )

class PostCreate(Schema):
    content: str
    hashtag: list

class PostUpdate(Schema):
    content: str = None
    hashtag: list = None

class UserSignIn(Schema):
    email: str
    password: str

class UserDetailSchema(Schema):
    name: str = None
    profilePhoto: str = None
    profileIntro: str = None
    phoneNumber: str = None
    gender: bool = None
    birth: str = None
