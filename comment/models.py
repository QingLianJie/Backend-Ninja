from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from common.models import BaseModel
from course.models import CourseInfo


class CourseComment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    course = models.ForeignKey(CourseInfo, on_delete=models.CASCADE, db_index=True)
    content = models.TextField(max_length=100)
    created = models.DateTimeField(default=timezone.now)
    anonymous = models.BooleanField(default=False)
    anonymous_name = models.CharField(max_length=32, db_index=True, default="匿名")
