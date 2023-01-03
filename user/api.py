from ninja import Router
from user.schemas import UserIn
from user.models import UserModel

router = Router()

@router.get("/home")
def home(request):
    return "Hello world!"

@router.get("/enter")
def enter(request, message):
    return f"Hi {message}"

@router.post("/signin", response=UserIn)
def signin(request, data: UserIn):
    #user = UserModel.objects.create()
    # print(dir(request))
    # print(request.POST.dict())
    return data