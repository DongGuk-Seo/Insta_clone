from ninja import Router
from ninja.errors import ValidationError
from ninja_jwt.authentication import JWTAuth
from ninja_extra.shortcuts import get_object_or_exception
from comments.schemas import CommentSchema
from posts.models import Post
from comments.models import Comment, Reply

router = Router()

@router.post('/{int:post_id}', auth=JWTAuth())
def create_comment(request, post_id, body:CommentSchema):
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.create(post=post,user=request.user,content=body.content)
    comment.save()
    return {"detail" : "댓글을 작성하셨습니다"}

@router.post('/{int:post_id}/{int:comment_id}', auth=JWTAuth())
def create_comment(request, post_id, comment_id, body:CommentSchema):
    comment = Comment.objects.get(id=comment_id)
    Reply = Reply(comment=comment,user=request.user,content=body.content)
    Reply.save()
    return {"detail" : "답글을 작성하셨습니다"}

@router.get('/{int:post_id}/{int:comment_id}')
def retrieve_comment(request, post_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    commentReplies = Reply.objects.filter(comment_id=comment_id)
    reply_data = []
    for Reply in commentReplies:
        dic = {}
        dic["replyId"] = Reply.id
        dic["username"] = Reply.user.username
        dic["userId"] = Reply.user.id
        dic["content"] = Reply.content
        dic["createdAt"] = Reply.createdAt
        reply_data.append(dic)

    data = {
        "commentId" : comment.id,
        "userId" : comment.user.id,
        "username": comment.user.username,
        "content" : comment.content,
        "commentReplies" : reply_data
    }
    return data

@router.put('/{int:post_id}/{int:comment_id}', auth=JWTAuth())
def update_comment(request, post_id, comment_id, body:CommentSchema):
    comment = Comment.objects.get(id=comment_id)
    if request.user == comment.user:
        comment.content = body.content
        comment.save()
        return {"detail" : "댓글을 수정하셨습니다"}
    raise ValidationError("유저가 일치하지 않습니다")

@router.put('/{int:post_id}/{int:comment_id}/{int:reply_id}', auth=JWTAuth())
def update_comment(request, post_id, comment_id, reply_id, body:CommentSchema):
    reply = Reply.objects.get(id=reply_id)
    if request.user == reply.user:
        reply.content = body.content
        reply.save()
        return {"detail" : "답글을 수정하셨습니다"}
    raise ValidationError("유저가 일치하지 않습니다")

@router.delete('/{int:post_id}/{int:comment_id}', auth=JWTAuth())
def create_comment(request, post_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user == comment.user:
        comment.delete()
        return {"detail" : "댓글을 삭제하셨습니다"}
    raise ValidationError("유저가 일치하지 않습니다")

@router.delete('/{int:post_id}/{int:comment_id}/{int:reply_id}', auth=JWTAuth())
def create_comment(request, post_id, comment_id, reply_id):
    reply = Reply.objects.get(id=reply_id)
    if request.user == reply.user:
        reply.delete()
        return {"detail" : "답글을 삭제하셨습니다"}
    raise ValidationError("유저가 일치하지 않습니다")