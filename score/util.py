from typing import List

from score.models import ScoreRecord
from score.schemas import ScoreRecordSchema


def select_by_heu_username_hash(heu_username_hash: str) -> List[ScoreRecordSchema]:
    return [ScoreRecordSchema.from_orm(x) for x in ScoreRecord.objects.filter(heu_username_hash=heu_username_hash)]
