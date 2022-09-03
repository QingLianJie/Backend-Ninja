import json

from django.db import models

from common.models import BaseModel
from course.models import CourseInfo


class ScoreRecord(BaseModel):
    heu_username_hash = models.CharField(max_length=128, db_index=True)
    score_raw_content_hash = models.CharField(max_length=128, db_index=True, unique=True)
    score = models.CharField(max_length=24)
    term = models.CharField(max_length=48)
    test = models.CharField(max_length=8)  # 考查方式（考试、考查等）
    course = models.ForeignKey(CourseInfo, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return " ".join([self.heu_username_hash, str(self.course), self.score])
