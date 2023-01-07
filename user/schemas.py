from django.contrib.auth.models import User
from ninja import ModelSchema, Schema

from user.models import UserProfileAvatar


class UserInfoSchema(ModelSchema):
    avatar: str = None

    class Config:
        model = User
        model_fields = ['id', 'username', 'date_joined']


class UserFullInfoSchema(ModelSchema):
    avatar: str = None

    class Config:
        model = User
        model_fields = ['id', 'username', 'date_joined', "email"]


class UserPhotoUploadSchema(ModelSchema):
    class Config:
        model = UserProfileAvatar
        model_fields = ['avatar']
