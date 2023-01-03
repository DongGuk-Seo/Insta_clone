from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from .manager import UserManager

# Create your models here.
class UserModel(AbstractUser):
    objects = UserManager()

    id = models.BigAutoField(unique=True, primary_key=True)
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
        max_length=50
    )
    username = models.CharField(
        unique=True,
        max_length=30
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = "username"

    class Meta:
        verbose_name = _("user")

    def __str__(self):
        return self.email

class UserDetailModel(models.Model):
    userId = models.ForeignKey(UserModel,related_name='userId', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    profileImage = models.ImageField(null=True, blank=True)
    profileIntro = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=20)
    gender = models.BooleanField()
    birth = models.DateTimeField()