from typing import List

from ninja import Router

from course.models import CourseInfo, CourseStatisticsResult
from course.schemas import CourseInfoSchema, CourseStatisticsResultSchema
from qinglianjie_ninja import settings

router = Router(tags=["Course"])

if settings.DEBUG:
    @router.get("/all", response=List[CourseInfoSchema])
    def get_all_courses(request):
        return [CourseInfoSchema.from_orm(x) for x in CourseInfo.objects.all()]


    @router.get("/statistics/all", response=List[CourseStatisticsResultSchema])
    def get_all_courses_statistics(request):
        return [CourseStatisticsResultSchema.from_orm(x) for x in CourseStatisticsResult.objects.all()]
