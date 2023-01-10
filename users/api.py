from ninja import Router
from ninja.errors import ValidationError
from users.schemas import UserSignUpSchema, UserSignInSchema
from users.models import User, UserDetail
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.authentication import JWTAuth

router = Router()

@router.post("/signup")
def sign_up(request, data: UserSignUpSchema):
    email = data.email
    username = data.username
    if '@' and '.' not in email:
        raise ValidationError("이메일 형식을 지켜주세요")
    if User.objects.filter(email=email).exists():
        raise ValidationError("이메일이 이미 존재합니다")
    if User.objects.filter(username=username).exists():
        raise ValidationError("유저 이름이 이미 존재합니다")
    user = User(email=email,username=username)
    user.set_password(data.password)
    user.save()
    userDetail = UserDetail(user.id)
    userDetail.save()
    return {"detail" : "회원가입을 성공하셨습니다"}

@router.post("/signin")
def sign_in(request, data: UserSignInSchema):
    email = data.email
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
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

@router.post("/follow/{int:follow_id}", auth=JWTAuth())
def user_follow(request, follow_id):
    if follow_id != request.user.id:
        user = User.objects.get(id=follow_id)
        if user.following.filter(id=request.user.id).exists():
            user.following.remove(request.user)
            return {"detail" : f"{user.username}님의 팔로우를 해지하셨습니다"}
        else:
            user.following.add(request.user)
            return {"detail" : f"{user.username}님을 팔로우하셨습니다"}
    raise ValidationError("본인 계정은 팔로우 할 수 없습니다")