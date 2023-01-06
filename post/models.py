from django.db import models
from user.models import UserModel
from datetime import datetime

# Create your models here.
def make_image_route(instance, file):
    time = datetime.now()
    return f'{instance.post_id}/{time.microsecond}_{file}'

class PostModel(models.Model):
    id = models.BigAutoField(primary_key=True,auto_created=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='post')
    content = models.CharField(max_length=500)
    postLike = models.ManyToManyField(UserModel, related_name="like")
    postBookmark = models.ManyToManyField(UserModel, related_name="bookmark")

class PostImageModel(models.Model):
    id = models.BigAutoField(primary_key=True,auto_created=True)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to=make_image_route)

class PostHashtagModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='hashtag')
    tagName = models.CharField(max_length=100)

class PostCommentModel(models.Model):
    id = models.BigAutoField(primary_key=True,auto_created=True)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comment_post')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='comment_user')
    content = models.CharField(max_length=200)

class PostCommentReplyModel(models.Model):
    id = models.BigAutoField(primary_key=True,auto_created=True)
    comment = models.ForeignKey(PostCommentModel, on_delete=models.CASCADE, related_name='reply_comment')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='reply_user')
    content = models.CharField(max_length=200)
