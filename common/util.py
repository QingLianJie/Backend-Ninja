import hashlib
from typing import Dict

from common.schemas import TestEnum


def increment(d: Dict, key: str, value: int):
    if key not in d.keys():
        d[key] = 0
    d[key] += value


def get_md5_hash_string(string: str) -> str:
    return hashlib.md5(string.encode(encoding='utf-8')).hexdigest()


def validate_score_type(value: str) -> TestEnum:
    valid_exam_score: bool = False
    valid_test_score: bool = value in ['不及格', '及格', '中等', '良好', '优秀']
    try:
        if 0 <= int(value) <= 100:
            valid_exam_score = True
    except Exception as e:
        valid_exam_score = False

    if valid_test_score:
        return TestEnum.test

    if valid_exam_score:
        return TestEnum.exam

    raise ValueError('成绩格式错误')
