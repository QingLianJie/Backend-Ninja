from django.db import models
from django.db.models import Model

from common.models import BaseModel
from course.consts import COURSE_DEFAULT_STATISTICS_RESULT


class CourseInfo(Model):
    id = models.CharField(max_length=32, unique=True, db_index=True, primary_key=True)  # 课程编号
    name = models.CharField(max_length=128, db_index=True)
    type = models.CharField(max_length=32, db_index=True)  # 类型（必修、选修等）
    category = models.CharField(max_length=64, db_index=True)  # 课程分类（选修中的艺术修养与审美、创新创业类等）
    test = models.CharField(max_length=8, db_index=True)  # 考查方式（考试、考查等）
    credit = models.FloatField(db_index=True)  # 学分
    nature = models.CharField(max_length=64, db_index=True)  # 课程性质（专业核心课程、自然科学与技术基础必修课等）
    period = models.FloatField(db_index=True)  # 学时
    count = models.IntegerField(default=0)  # 学过的人数

    def __str__(self):
        return " ".join([str(self.id), str(self.name)])


class CourseStatisticsResult(Model):
    course = models.ForeignKey(CourseInfo, on_delete=models.CASCADE, db_index=True)
    statistics = models.TextField(default=COURSE_DEFAULT_STATISTICS_RESULT)

    def __str__(self):
        return str(self.course)
