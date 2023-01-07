from ninja import Router
from ninja.errors import ValidationError
from ninja_jwt.authentication import JWTAuth
from ninja_extra.shortcuts import get_object_or_exception
from comment.schemas import CommentCreate
from post.models import PostModel
from comment.models import CommentModel

router = Router()

@router.post('/{int:post_id}', auth=JWTAuth())
def create_comment(request, post_id, body:CommentCreate):
    post = PostModel.objects.get(id=post_id)
    comment = CommentModel.objects.create(post=post,user=request.user,content=body.content)
    comment.save()
    return {"detail" : "댓글을 작성하셨습니다"}