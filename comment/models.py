from django.db import models
from django.utils import timezone
from post.models import PostModel
from user.models import UserModel

# Create your models here.

class CommentModel(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='comment')
    content = models.CharField(max_length=200)
    createdAt = models.DateTimeField(default=timezone.now)

class ReplyModel(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='comment_reply')
    comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE, related_name='comment_reply')
    content = models.CharField(max_length=200)
    createdAt = models.DateTimeField(default=timezone.now)