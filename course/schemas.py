import datetime
from typing import Dict

from ninja import Schema, ModelSchema
from pydantic import Json

from course.models import CourseInfo


class CourseInfoSchema(ModelSchema):
    class Config:
        model = CourseInfo
        model_fields = [
            'id',  # 课程编号
            'name',
            'type',  # 类型（必修、选修等）
            'category',  # 课程分类（选修中的艺术修养与审美、创新创业类等）
            'test',  # 考查方式（考试、考查等）
            'credit',  # 学分
            'nature',  # 课程性质（专业核心课程、自然科学与技术基础必修课等）
            'period',  # 学时
            # 'count', # 学过的人数
        ]


class CourseStatisticsRecordSchema(Schema):
    total: int = 0
    exam: Dict[str, int] = {}
    test: Dict[str, int] = {}


class CourseStatisticsResultSchema(Schema):
    course: CourseInfoSchema
    statistics: Json[Dict[str, CourseStatisticsRecordSchema]]
