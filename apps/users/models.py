from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=32)
    discord_id = models.IntegerField()
    password = None

    objects = UserManager()
    USERNAME_FIELD = 'id'

    def __str__(self):
        return str(self.username)

    class Meta:
        permissions = (
            ('is_admin', 'User is administrator'),
        )

