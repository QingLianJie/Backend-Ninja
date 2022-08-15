from django.contrib.auth.models import User
from django.db import models

from common.models import BaseModel


class PasswordResetVerifyCode(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="请求重置密码的用户")
    verify_code = models.CharField(max_length=24, verbose_name="验证码")
