from django.contrib.auth.models import User
from django.db import models

from common.models import BaseModel
from course.models import CourseInfo


class UploadHashInfo(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    hash = models.CharField(max_length=128, db_index=True)
    
    def __str__(self):
        return " ".join([self.user])
