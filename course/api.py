from typing import List

from ninja import Router
from ninja.pagination import paginate

from comment.models import CourseComment
from comment.schemas import CourseCommentResponseSchema
from common.schemas import Error
from course.models import CourseInfo, CourseStatisticsResult
from course.schemas import CourseInfoSchema, CourseStatisticsResultSchema, CourseInfoPageResponseSchema
from qinglianjie_ninja import settings

router = Router(tags=["Course"])


@router.get("/search/", response=List[CourseInfoSchema])
@paginate
def search_course(request,
                  content: str = "",
                  type: str = None,
                  category: str = None,
                  test: str = None,
                  credit: float = None,
                  period: float = None):
    filter_fields = ['type', 'category', 'test', 'credit', 'period']
    query_dict = {}
    for field in filter_fields:
        value = locals()[field]
        if value is not None:
            query_dict[field] = value
    results = CourseInfo.objects.filter(id__contains=content, **query_dict) | \
              CourseInfo.objects.filter(name__contains=content, **query_dict)
    return [CourseInfoSchema.from_orm(x) for x in results]


@router.get("/{course_id}/", response={404: Error, 200: CourseInfoPageResponseSchema})
def get_course_detailed_info_by_course_id(request, course_id: str):
    try:
        statistics = CourseStatisticsResult.objects.get(course__id=course_id)
        comments = CourseComment.objects.filter(course__id=course_id).order_by('-create_time')[:20]
        more_comments: bool = CourseComment.objects.filter(course__id=course_id).count() >= 50
        return CourseInfoPageResponseSchema(
            course=statistics.course,
            statistics=statistics.statistics,
            comments=[CourseCommentResponseSchema.my_from_orm(x) for x in comments],
            more_comments=more_comments,
        )
    except CourseStatisticsResult.DoesNotExist:
        return 404, {'detail': "课程 id 不存在"}


if settings.DEBUG:
    @router.get("/statistics/all/", response=List[CourseStatisticsResultSchema], description="!!!测试用接口!!!", summary="!!!测试用接口!!!")
    def get_all_courses_statistics(request):
        return [CourseStatisticsResultSchema.from_orm(x) for x in CourseStatisticsResult.objects.all()]
