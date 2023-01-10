from ninja import Schema

class UserSignUpSchema(Schema):
    email: str
    password: str
    username: str

class UserSignInSchema(Schema):
    email: str
    password: str

class UserDetailSchema(Schema):
    name: str = None
    profile_photo: str = None
    profile_intro: str = None
    phone_number: str = None
    gender: bool = None
    birth: str = None
