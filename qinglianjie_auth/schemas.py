from django.contrib.auth.models import User
from ninja import ModelSchema, Schema
from pydantic import Field


class UserBaseSchema(ModelSchema):
    class Config:
        model = User
        model_fields = ['id', 'username', 'email']


class UsernameLoginSchema(ModelSchema):
    password: str = Field(min_length=8, max_length=24)

    class Config:
        model = User
        model_fields = ['username']


class EmailLoginSchema(ModelSchema):
    password: str = Field(min_length=8, max_length=24)

    class Config:
        model = User
        model_fields = ['email']


class UserRegisterSchema(ModelSchema):
    password: str = Field(min_length=8, max_length=24)

    class Config:
        model = User
        model_fields = ['email', "username"]


class RequestPasswordResetInputSchema(Schema):
    email: str


class PasswordResetInputSchema(Schema):
    email: str
    verify_code: str
    new_password: str = Field(min_length=8, max_length=24)


class PasswordChangeInputSchema(Schema):
    old_password: str = Field(min_length=8, max_length=24)
    new_password: str = Field(min_length=8, max_length=24)
