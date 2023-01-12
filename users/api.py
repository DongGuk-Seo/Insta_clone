from ninja import Router
from ninja.errors import ValidationError
from users.schemas import UserSignUpSchema, UserSignInSchema
from users.models import User, UserDetail, UserFollow
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
def user_follow(request, follow_id:int):
    if follow_id != request.user.id:
        user = UserFollow.objects.filter(user_id=request.user.id)
        check_user = user.filter(follow_id=follow_id)
        follow_user = User.objects.get(id=follow_id)
        if check_user.exists():
            check_user.get(follow_id=follow_id).delete()
            return {"detail" : f"{follow_user.username}님의 팔로우를 해지하셨습니다"}
        else:
            UserFollow.objects.create(user_id=request.user.id, follow_id=follow_id)
            return {"detail" : f"{follow_user.username}님을 팔로우하셨습니다"}
    raise ValidationError("본인 계정은 팔로우 할 수 없습니다")

@router.get("/following/{int:user_id}", auth=JWTAuth())
def get_user_following(request, user_id:int):
    user_following = UserFollow.objects.select_related('follow').filter(user_id=user_id).order_by('-user_id')
    users = []
    for user in user_following:
        user_dic = {}
        user_id_ = user.follow_id
        user_dic["user_id"] = user_id_
        user_dic["username"] = user.follow.username
        user_dic["profile_image"] = UserDetail.objects.get(user_id=user_id_).profile_image.url
        users.append(user_dic)
    return users

@router.get("/follower/{int:user_id}", auth=JWTAuth())
def get_user_follower(request, user_id:int):
    user_follower = UserFollow.objects.select_related('follow').filter(follow_id=user_id).order_by('-user_id')
    users = []
    for user in user_follower:
        user_dic = {}
        user_id_ = user.user_id
        user_dic["user_id"] = user_id_
        user_dic["username"] = user.user.username
        user_dic["profile_image"] = UserDetail.objects.get(user_id=user_id_).profile_image.url
        users.append(user_dic)
    return users