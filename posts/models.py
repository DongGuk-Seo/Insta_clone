from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

# Create your models here.
def make_image_route(instance, file):
    time = datetime.now()
    return f'{instance.post_id}/{time.microsecond}_{file}'

class Post(models.Model):
    id = models.BigAutoField(primary_key=True,auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    content = models.CharField(max_length=500)

class PostImage(models.Model):
    id = models.BigAutoField(primary_key=True,auto_created=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to=make_image_route)

class PostHashtag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='hashtag')
    tag_name = models.CharField(max_length=100)

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like')

class PostBookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmark')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmark')