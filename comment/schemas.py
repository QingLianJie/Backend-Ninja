from typing import List

from ninja import Schema, ModelSchema
from pydantic import Field

from comment.models import CourseComment
from qinglianjie_auth.schemas import UserBaseSchema


class CourseCommentRequestSchema(ModelSchema):
    class Config:
        model = CourseComment
        model_fields = [
            'content',
            'anonymous',
            'anonymous_name',
        ]


class CourseCommentResponseSchema(ModelSchema):
    user: UserBaseSchema = None
    anonymous_name: str = Field(None)

    @classmethod
    def my_from_orm(cls, obj):
        result = CourseCommentResponseSchema.from_orm(obj)
        if result.anonymous == True:
            result.user = None
        return result

    class Config:
        model = CourseComment
        model_fields = [
            "id",
            'content',
            'created',
            'anonymous',
        ]


class AnonymousAliasResponseSchema(Schema):
    alias: List[str]  # 别名列表
    max_alias_count: int  # 最大可创建别名数量
    spent_alias_count: int  # 已创建别名数
