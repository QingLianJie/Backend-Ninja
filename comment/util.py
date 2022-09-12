import math

from django.contrib.auth.models import User
from django.utils import timezone

from comment.consts import MAX_ANONYMOUS_ALIAS_NUMBER
from comment.models import AnonymousCreatedCount, AnonymousAlias


def get_spent_alias_count(user: User) -> int:
    # 查询已消耗的别名创建机会数量
    result = 0
    try:
        record = AnonymousCreatedCount.objects.get(user=user)
        result = record.count
    except AnonymousCreatedCount.DoesNotExist as e:
        pass
    return max(result, AnonymousAlias.objects.filter(user=user).count())


def get_max_alias_count(user: User) -> int:
    # 根据注册时间计算可用别名个数上限，一年增加一个
    delta = timezone.now() - user.date_joined
    max_alias_count = min(MAX_ANONYMOUS_ALIAS_NUMBER, max(int(math.ceil(delta.days / 365.0)), 1))
    return max_alias_count
