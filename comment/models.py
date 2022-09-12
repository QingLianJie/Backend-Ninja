from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from comment.consts import DEFAULT_ANONYMOUS_DISPLAY_NAME
from common.models import BaseModel
from course.models import CourseInfo


class CourseComment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    course = models.ForeignKey(CourseInfo, on_delete=models.CASCADE, db_index=True)
    content = models.TextField(max_length=100)
    created = models.DateTimeField(default=timezone.now)
    anonymous = models.BooleanField(default=False)
    anonymous_name = models.CharField(max_length=32, db_index=True, default=DEFAULT_ANONYMOUS_DISPLAY_NAME, null=True)


class AnonymousAlias(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, unique=True)
    alias = models.CharField(max_length=32, unique=True)


class AnonymousCreatedCount(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    count = models.IntegerField(default=0)
