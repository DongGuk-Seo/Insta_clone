from django.db import models
from post.models import PostModel
from user.models import UserModel

# Create your models here.

class CommentModel(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='comment')
    content = models.CharField(max_length=200)