import random

import django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
from ninja import Router, Body
from ninja.security import django_auth

from comment.models import AnonymousAlias
from qinglianjie_auth import logger
from qinglianjie_auth.consts import AUTH_VERIFY_CODE_EXPIRE_SECONDS, AUTH_VERIFY_CODE_LENGTH, \
    AUTH_RESET_PASSWORD_EMAIL_TITLE, AUTH_RESET_PASSWORD_EMAIL_BODY
from qinglianjie_auth.models import PasswordResetVerifyCode
from qinglianjie_auth.schemas import UsernameLoginSchema, UserRegisterSchema, UserBaseSchema, EmailLoginSchema, \
    RequestPasswordResetInputSchema, PasswordResetInputSchema, PasswordChangeInputSchema
from common.schemas import Error
from qinglianjie_ninja.settings import EMAIL_FROM

router = Router(tags=["Auth"])


@router.post("/register/", response={200: UserBaseSchema, 400: Error}, description="注册账户")
def register(request, data: UserRegisterSchema):
    if User.objects.filter(username=data.username).count() != 0 \
            or AnonymousAlias.objects.filter(alias=data.username).count() != 0 \
            or User.objects.filter(email=data.email).count() != 0:
        return 400, {'detail': "用户名或邮箱已被占用"}
    user = User.objects.create_user(**data.dict())
    login(request, user)
    return 200, user


@router.post("/login/username/", auth=None, response={200: UserBaseSchema, 400: Error}, description="通过用户名登陆")
def login_by_username(request, data: UsernameLoginSchema):
    user = authenticate(**data.dict())
    if user is not None and user.is_active:
        login(request, user)
        return 200, user
    return 400, {'detail': "用户名或密码错误"}


@router.post("/login/email/", auth=None, response={200: UserBaseSchema, 400: Error}, description="通过邮件登录")
def login_by_email(request, data: EmailLoginSchema):
    try:
        username = User.objects.get(email=data.email).username
        user = authenticate(username=username, password=data.password)
    except django.contrib.auth.models.User.DoesNotExist as e:
        logger.debug(e)
        user = None

    if user is not None and user.is_active:
        login(request, user)
        return 200, user

    return 400, {'detail': "邮箱或密码错误"}


@router.delete("/logout/", auth=django_auth, response={204: None}, description="登出当前账户")
def logout_api(request):
    logout(request)
    return 204, None


# @router.get('/me/', response=UserBaseSchema, auth=django_auth, description="返回当前登录用户信息")
# def me(request):
#     return request.user


@router.post("/password/change/", auth=django_auth, description="修改密码", response={400: Error, 204: None})
def change_password(request, data: PasswordChangeInputSchema):
    if data.old_password == data.new_password:
        return 400, {"detail": "新旧密码不能相同！"}

    user = request.user
    user_temp = authenticate(username=user.username, password=data.old_password)
    if user_temp is None or user.id != user_temp.id:
        return 400, {"detail": "旧密码错误！"}

    # 修改密码
    with transaction.atomic():
        user.set_password(data.new_password)
        user.save()
    return 204, None


@router.post("/password/reset/", description="请求重置密码", response={204: None, 404: Error, 400: Error}, auth=None)
def request_reset_password(request, data: RequestPasswordResetInputSchema):
    try:
        user = User.objects.get(email=data.email)
    except django.contrib.auth.models.User.DoesNotExist as e:
        user = None

    if user is None or user.is_superuser:
        return 404, {"detail": "邮箱不存在"}

    with transaction.atomic():
        PasswordResetVerifyCode.objects.filter(user=user).delete()
        # 随机验证码
        limit = 10 ** AUTH_VERIFY_CODE_LENGTH
        verify_code: str = str(random.randint(0, limit)).zfill(AUTH_VERIFY_CODE_LENGTH)
        PasswordResetVerifyCode.objects.create(user=user, verify_code=verify_code).save()
        logger.info(f"{user} 请求重置密码，验证码为: {verify_code}")

        # 发送邮件
        try:
            send_mail(
                AUTH_RESET_PASSWORD_EMAIL_TITLE,
                AUTH_RESET_PASSWORD_EMAIL_BODY.format(verify_code, user.username),
                EMAIL_FROM,
                [data.email])
        except Exception as e:
            logger.error(f"密码重置邮件 To {user.email}({user.username}) 发送失败")
            logger.error(e)
            return 400, {"detail": "邮件发送失败，请稍后再试！"}

    return 204, None


@router.put("/password/reset/", description="重置密码", auth=None, response={204: None, 400: Error})
def reset_password(request, data: PasswordResetInputSchema):
    try:
        verify_code_record = PasswordResetVerifyCode.objects.get(verify_code=data.verify_code)
    except Exception as e:
        logger.debug(e)
        verify_code_record = None

    # 验证码不存在或邮箱不匹配
    if verify_code_record is None or verify_code_record.user.email != data.email:
        return 400, {"detail": "验证码有误或不存在"}

    # 检查验证码是否过期
    detail = timezone.now() - verify_code_record.create_time
    if detail.total_seconds() >= AUTH_VERIFY_CODE_EXPIRE_SECONDS:
        verify_code_record.delete()
        return 400, {"detail": "验证码有误或不存在"}

    with transaction.atomic():
        user = verify_code_record.user
        user.set_password(data.new_password)
        verify_code_record.delete()
        user.save()

    logger.info(f"{user} reset password successfully.")

    return 204, None
