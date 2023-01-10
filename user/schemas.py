from ninja import Schema, ModelSchema
from user.models import UserModel, UserDetailModel

class UserSignUp(Schema):
    email: str
    password: str
    username: str

class UserSignIn(Schema):
    email: str
    password: str

class UserDetailSchema(Schema):
    name: str = None
    profile_photo: str = None
    profile_intro: str = None
    phone_number: str = None
    gender: bool = None
    birth: str = None
