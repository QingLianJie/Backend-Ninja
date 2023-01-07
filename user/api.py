from typing import Optional, List

from django.contrib.auth.models import User
from ninja import Router, File, UploadedFile, Form
from ninja.security import django_auth

from comment.models import CourseComment
from comment.schemas import CourseCommentResponseSchema
from common.schemas import Error
from qinglianjie_ninja import settings
from user.models import UserProfileAvatar
from user.schemas import UserInfoSchema, UserFullInfoSchema

router = Router(tags=["User"])


@router.get("/me", auth=django_auth, response=UserFullInfoSchema)
def get_my_user_info(request):
    user: User = request.user
    user_info = UserFullInfoSchema.from_orm(user)
    try:
        photo_in_db, created = UserProfileAvatar.objects.get_or_create(user=user)
        user_info.avatar = photo_in_db.avatar.url
    except ValueError as e:
        user_info.avatar = None
    return 200, user_info


@router.post("/avatar/", auth=django_auth, response={200: None, 400: Error})
def update_user_avatar(request, image: UploadedFile = File(...)):
    if str(image.content_type).split("/")[0] != 'image':
        return 400, {"detail": "请勿上传非图片文件"}
    if image.size >= settings.MAX_AVATAR_SIZE * 1024.0 * 1024.0:
        return 400, {"detail": f'头像文件大小限制为 ${settings.MAX_AVATAR_SIZE} MB'}

    user: User = request.user
    photo_in_db, created = UserProfileAvatar.objects.get_or_create(user=user)
    if not created:
        try:
            photo_in_db.avatar.delete()
        except Exception as e:
            print(e)
    photo_in_db.avatar = image
    photo_in_db.save()
    return 200, None


@router.delete("/avatar/", auth=django_auth, response={200: None})
def delete_user_avatar(request):
    user: User = request.user
    photo_in_db, created = UserProfileAvatar.objects.get_or_create(user=user)
    try:
        photo_in_db.avatar.delete()
    except Exception as e:
        print(e)
    return 200, None


@router.delete("/delete/user/")
def delete_all_user_info():
    pass


@router.get("/{username}/", response={200: UserInfoSchema, 404: Error})
def get_user_info_by_username(request, username: str):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist as e:
        return 404, {"detail": "用户不存在"}

    user_info = UserInfoSchema.from_orm(user)
    try:
        photo_in_db, created = UserProfileAvatar.objects.get_or_create(user=user)
        user_info.avatar = photo_in_db.avatar.url
    except ValueError as e:
        user_info.avatar = None
    return 200, user_info


@router.get("/{username}/comments", response={200: List[CourseCommentResponseSchema], 400: Error})
def get_user_comments(request, username: str):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist as e:
        return 404, {"detail": "用户不存在"}

    return [comment for comment in CourseComment.objects.filter(user=user, anonymous=False)]
