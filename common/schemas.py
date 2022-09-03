from enum import Enum

from ninja import Schema


class Error(Schema):
    detail: str


class TestEnum(str, Enum):
    test = '考查'
    exam = '考试'
    other = '其他'