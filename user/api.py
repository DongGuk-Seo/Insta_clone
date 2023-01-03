from ninja import Router
from ninja.errors import ValidationError
from user.schemas import UserSignUp, UserSignIn
from user.models import UserModel, UserDetailModel
from ninja_jwt.tokens import RefreshToken

router = Router()

@router.post("/signup")
def signup(request, data: UserSignUp):
    email = data.email
    username = data.username
    if '@' and '.' not in email:
        raise ValidationError("이메일 형식을 지켜주세요")
    if UserModel.objects.filter(email=email).exists():
        raise ValidationError("이메일이 이미 존재합니다")
    if UserModel.objects.filter(username=username).exists():
        raise ValidationError("유저 이름이 이미 존재합니다")
    user = UserModel(email=email,username=username)
    user.set_password(data.password)
    user.save()
    userDetail = UserDetailModel(user.id)
    userDetail.save()
    return {"detail" : "회원가입을 성공하셨습니다"}

@router.post("/signin")
def signin(request, data: UserSignIn):
    email = data.email
    if UserModel.objects.filter(email=email).exists():
        user = UserModel.objects.get(email=email)
        if user.check_password(data.password):
            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)
            return {
                "username":user.username,
                "accessToken":access,
                "refreshToken" : refresh, 
                }
        raise ValidationError("틀린 비밀번호 입니다")
    raise ValidationError("이메일이 존재하지 않습니다")