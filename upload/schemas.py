from typing import List

from ninja import Schema
from pydantic import validator

from common.schemas import TestEnum
from common.util import validate_score_type


def by_pass(string: str) -> str:
    return string if string != 'from_' else 'form'


class ScoreUploadSchema(Schema):
    term: str  # 学期
    name: str  # 课程名称
    id: str  # 课程 id
    type: str  # 类型（必修、选修等）
    test: TestEnum  # 考查方式（考试、考查等）
    from_: List[str]  # 考试性质（正常考试、缺考等）
    credit: float  # 学分
    period: float  # 学时
    score: str  # 分数（分数制或等级制）
    category: str  # 课程分类（选修中的艺术修养与审美、创新创业类等）
    mark: List[str]  # 成绩标记（如缺考）

    class Config(Schema.Config):
        alias_generator = by_pass

    @validator('score')
    def validate_score(cls, v, values, **kwargs):
        t = validate_score_type(v)
        valid_exam_score: bool = t == TestEnum.exam
        valid_test_score: bool = t == TestEnum.test
        if values['test'] == TestEnum.exam and not valid_exam_score:
            raise ValueError('考试课成绩格式错误')
        if values['test'] == TestEnum.test and not valid_test_score:
            raise ValueError('考察课成绩格式错误')
        if values['test'] == TestEnum.other and not valid_exam_score and not valid_test_score:
            raise ValueError('其他课成绩格式错误')
        return v


class UploadDataSchema(Schema):
    # score_hash: str  # score 的 MD5 摘要值
    heu_username_hash: str  # 学号经 MD5 摘要
    scores: List[ScoreUploadSchema]
    # date: datetime.datetime
    # grade: int  # 年级 2018 2019 等
