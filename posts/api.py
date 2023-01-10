from ninja import Router, Form, File
from ninja.files import UploadedFile
from ninja.errors import ValidationError
from ninja_jwt.authentication import JWTAuth
from ninja_extra.shortcuts import get_object_or_exception
from typing import List
from posts.schemas import PostCreateSchema, PostUpdateSchema
from posts.models import (
    Post, 
    PostImage, 
    PostHashtag,
    PostLike,
    PostBookmark
    )

router = Router()

@router.post("", auth=JWTAuth())
def create_post(request, data:PostCreateSchema = Form(default=None), images:List[UploadedFile]=File(default=None)):
    post = Post(user=request.user,content=data.content)
    post.save()
    if data.hashtag != None:
        tags = data.hashtag
        for tag in tags:
            tag_ = PostHashtag(post=post, tag_name=tag)
            tag_.save()
    if images != None:
        for image in images:
            image_ = PostImage(post=post, image=image)
            image_.save()
    return {"detail" : "게시글을 작성하셨습니다"}

@router.get("/{int:post_id}")
def retrieve_post(request, post_id:int):
    post = get_object_or_exception(Post, id=post_id)
    images = [obj.image.url for obj in PostImage.objects.filter(post=post_id)]
    tags = [obj.tag_name for obj in PostHashtag.objects.filter(post=post_id)]
    data = {
        "content" : post.content,
        "images" : images,
        "tags" : tags
    }
    return data

@router.put("/{int:post_id}/content", auth=JWTAuth())
def update_post_content(request, post_id:int, data:PostUpdateSchema):
    post = Post.objects.get(id=post_id)
    if request.user == post.user:
        if data.content != None:
            setattr(post,'content',data.content)
            post.save()
        if data.hashtag != None:
            tags = PostHashtag.objects.filter(post=post)
            remain_tags_list = [tag.tag_name for tag in tags]
            for hashtag in data.hashtag:
                if hashtag not in remain_tags_list:
                    tag = PostHashtag(post=post, tag_name=hashtag)
                    tag.save()
                else:
                    remain_tags_list.remove(hashtag)
            for remain in remain_tags_list:
                tem = PostHashtag.objects.get(post=post, tag_name=remain)
                tem.delete()
        return {"detail" : "게시글 내용을 수정하셨습니다"}
    raise ValidationError({"detail" : "게시글 작성자가 일치하지 않습니다"})

@router.post("/{int:post_id}/image", auth=JWTAuth())
def update_post_image(request, post_id, images:List[UploadedFile]=File(default=None)):
    post = Post.objects.get(id=post_id)
    if request.user == post.user:
        for image in images:
            image_ = PostImage(post_id=post_id, image=image)
            image_.save()
        return {"detail" : "게시글 사진을 수정하셨습니다"}
    raise ValidationError({"detail" : "게시글 작성자가 일치하지 않습니다"})

@router.delete("/{int:post_id}", auth=JWTAuth())
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user == post.user:
        post.delete()
        return {"detail" : "게시글을 삭제하셨습니다"}
    raise ValidationError({"detail" : "게시글 작성자가 일치하지 않습니다"})

@router.delete("/{int:post_id}/{str:image_name}", auth=JWTAuth())
def delete_post(request, post_id, image_name):
    post = Post.objects.get(id=post_id)
    if request.user == post.user:
        image = get_object_or_exception(PostImage, post=post, image=f'{post_id}/{image_name}')
        image.delete()
        return {"detail" : "사진을 삭제하셨습니다"}
    raise ValidationError({"detail" : "게시글 작성자가 일치하지 않습니다"})

@router.post("/like/{int:post_id}", auth=JWTAuth())
def post_like(request, post_id):
    like_post = PostLike.objects.filter(post_id=post_id, user_id=request.user.id)
    if like_post.exists():
        like_post.delete()
        return {"detail" : "좋아요를 취소하셨습니다"}
    else:
        like_post.create(post_id=post_id,user_id=request.user.id)
        return {"detail" : "좋아요를 설정하셨습니다"}