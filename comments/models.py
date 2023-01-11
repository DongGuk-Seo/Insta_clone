from django.db import models
from django.utils import timezone
from posts.models import Post
from users.models import User

# Create your models here.

class Comment(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    content = models.CharField(max_length=200)
    createdAt = models.DateTimeField(default=timezone.now)

class Reply(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reply')
    content = models.CharField(max_length=200)
    createdAt = models.DateTimeField(default=timezone.now)