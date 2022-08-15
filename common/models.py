from django.db import models
from django.db.models import Model


class BaseModel(Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="记录创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="记录最后修改时间")
