from typing import List

from django.contrib.auth.models import User
from django.db import transaction
from ninja import Router, Body
from ninja.pagination import paginate
from ninja.security import django_auth

from comment.consts import MAX_ANONYMOUS_ALIAS_NUMBER, DEFAULT_ANONYMOUS_DISPLAY_NAME
from comment.models import AnonymousAlias, CourseComment, AnonymousCreatedCount
from comment.schemas import AnonymousAliasResponseSchema, CourseCommentResponseSchema, CourseCommentRequestSchema
from comment.util import get_spent_alias_count, get_max_alias_count
from common.schemas import Error
from course.models import CourseInfo

router = Router(tags=["Comment"])


@router.post("/alias/", description="新建匿名别名", response={400: Error, 201: str}, auth=django_auth)
def create_new_alias(request, alias: str = Body(..., min_length=1, max_length=32)):
    user: User = request.user

    spent_alias_number = get_spent_alias_count(user)
    max_alias_number = get_max_alias_count(user)
    if spent_alias_number >= max_alias_number:
        return 400, {'detail': f'别名创建次数已达上限 {max_alias_number} 个'}

    if (AnonymousAlias.objects.filter(alias=alias).count() +
        (User.objects.filter(username=alias) | User.objects.filter(email=alias)).count() +
        CourseComment.objects.filter(anonymous_name=alias).count()) != 0 \
            or alias == DEFAULT_ANONYMOUS_DISPLAY_NAME:
        return 400, {'detail': '别名已被占用'}

    with transaction.atomic():
        AnonymousAlias.objects.create(user=user, alias=alias).save()
        record, flag = AnonymousCreatedCount.objects.get_or_create(user=user)
        record.count = (0 if flag else record.count) + 1
        record.save()

    return 201, alias


@router.get("/alias/", description="列出当前账号所拥有的别名", response=AnonymousAliasResponseSchema, auth=django_auth)
def list_my_alias(request):
    return AnonymousAliasResponseSchema(
        alias=[record.alias for record in AnonymousAlias.objects.filter(user=request.user)],
        max_alias_count=get_max_alias_count(request.user),
        spent_alias_count=get_spent_alias_count(request.user),
    )


@router.delete("/alias/", description="删除指定别名", response={400: Error, 204: None}, auth=django_auth)
def delete_my_alias(request, alias: str = Body(..., min_length=1, max_length=32)):
    if AnonymousAlias.objects.filter(user=request.user, alias=alias).count() == 0:
        return 400, {'detail': "别名不存在"}
    if CourseComment.objects.filter(anonymous_name=alias).count() != 0:
        return 400, {'detail': "该别名下存在未删除的评论"}
    AnonymousAlias.objects.filter(user=request.user, alias=alias).delete()
    return None


@router.get("/my/", description="获取我发表的评论", auth=django_auth, response=List[CourseCommentResponseSchema])
@paginate
def get_my_comments(request):
    return [CourseCommentResponseSchema.my_from_orm(x) for x in CourseComment.objects.filter(user=request.user)]


@router.post("/{course_id}/", description="新建课程评论", auth=django_auth,
             response={201: CourseCommentResponseSchema, 400: Error, 404: Error})
def create_comment(request, course_id: str, data: CourseCommentRequestSchema):
    user: User = request.user

    # Check if course exists
    try:
        course = CourseInfo.objects.get(id=course_id)
    except CourseInfo.DoesNotExist as e:
        return 404, {'detail': '课程不存在'}

    if data.anonymous == False:
        data.anonymous_name = None

    # Check if alias exists
    if data.anonymous_name != DEFAULT_ANONYMOUS_DISPLAY_NAME and data.anonymous_name is not None:
        try:
            alias = AnonymousAlias.objects.get(user=user, alias=data.anonymous_name)
        except AnonymousAlias.DoesNotExist as e:
            return 400, {'detail': '非法请求'}

    comment = CourseComment.objects.create(**data.dict(), course_id=course_id, user_id=user.id)
    comment.save()
    return 201, CourseCommentResponseSchema.my_from_orm(comment)


@router.delete("delete/{comment_id}/",
               description="删除课程评论",
               auth=django_auth,
               response={400: Error, 404: Error, 204: None})
def delete_comment(request, comment_id: str):
    try:
        comment = CourseComment.objects.get(id=comment_id)
    except CourseComment.DoesNotExist as e:
        return 404, {'detail': '评论不存在'}
    if comment.user.pk != request.user.pk:
        return 400, {'detail': '非法请求'}

    comment.delete()
    return 204, None


@router.get("/{course_id}/", description="获取课程评论", response={404: Error, 200: List[CourseCommentResponseSchema]})
@paginate
def get_all_comments_of_course(request, course_id: str):
    try:
        course = CourseInfo.objects.get(id=course_id)
    except CourseInfo.DoesNotExist as e:
        return 404, {'detail': '课程不存在'}
    return [CourseCommentResponseSchema.my_from_orm(x) for x in CourseComment.objects.filter(course__id=course_id)]
