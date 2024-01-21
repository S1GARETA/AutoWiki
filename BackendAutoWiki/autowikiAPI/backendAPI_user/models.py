import uuid

from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from .managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=30, unique=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()
    def save(self, *args, **kwargs):
        # Если у пользователя еще нет username, сгенерировать его
        if not self.username:
            self.username = f"username_{uuid.uuid4().hex}"

        super().save(*args, **kwargs)

    def get_username(self):
        return self.username

    def __str__(self):
        return self.email

class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="User")
    item_type = models.CharField(max_length=50)
    item_id = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.item_type} {self.item_id}"
