import os

from django.contrib.auth.models import User
from django.db import models

from common.models import BaseModel
from user.util import user_directory_path


class UserProfileAvatar(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    avatar = models.ImageField(
        os.path.join("profile", "avatar"),
        upload_to=user_directory_path,
        null=True,
    )

    def __str__(self):
        return str(self.user)
