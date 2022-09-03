import datetime
import json
from typing import Dict, List

from django.db import transaction
from ninja import Schema, ModelSchema
from pydantic import Json

from common.util import increment, get_md5_hash_string, validate_score_type
from course.models import CourseStatisticsResult, CourseInfo
from course.schemas import CourseInfoSchema, CourseStatisticsResultSchema, CourseStatisticsRecordSchema
from score import logger
from score.models import ScoreRecord
from upload.schemas import ScoreUploadSchema
from common.schemas import TestEnum


class ScoreRecordSchema(ModelSchema):
    course: CourseInfoSchema

    class Config:
        model = ScoreRecord
        model_fields = [
            'heu_username_hash',
            'score_raw_content_hash',
            'score',
            'term',
            'test',
        ]

    @classmethod
    def from_raw_score_content(cls, heu_username_hash: str, score_record: ScoreUploadSchema):
        return ScoreRecordSchema(
            course=CourseInfoSchema.from_orm(CourseInfo.objects.get(id=score_record.id)),
            heu_username_hash=heu_username_hash,
            score_raw_content_hash=get_md5_hash_string(score_record.json()),
            score=score_record.score,
            term=score_record.term,
            test=score_record.test,
        )

    def update_statistics(self, undo: bool = False):
        with transaction.atomic():
            course_statistics_in_db: CourseStatisticsResult = \
                CourseStatisticsResult.objects.select_for_update().filter(course__id=self.course.id).first()
            course_statistics = CourseStatisticsResultSchema.from_orm(course_statistics_in_db)

            statistics_dict: Dict[str, CourseStatisticsRecordSchema] = course_statistics.statistics
            # If it's the first score record in statistics result, create it
            if self.term not in statistics_dict.keys():
                statistics_dict[self.term] = CourseStatisticsRecordSchema()

            statistics_dict[self.term].total += -1 if undo else 1

            # Update statistics result
            value = self.score
            if validate_score_type(value) == TestEnum.exam:
                increment(statistics_dict[self.term].exam, value, -1 if undo else 1)
                increment(statistics_dict['all'].exam, value, -1 if undo else 1)
            else:
                increment(statistics_dict[self.term].test, value, -1 if undo else 1)
                increment(statistics_dict['all'].test, value, -1 if undo else 1)

            # TODO: find a better way do encode
            course_statistics_in_db.statistics = json.dumps(json.loads(course_statistics.json())['statistics'])
            course_statistics_in_db.save()

            # Save or remove change log to db
            self._del_in_db() if undo else self._save_in_db()

            logger.info(f"{'Undo' if undo else 'Update'}' [{self.course.id}]{self.course.name} course statistics:")
            logger.info(statistics_dict)

    def _save_in_db(self):
        try:
            ScoreRecord.objects.create(**self.dict(exclude={'course'}), course_id=self.course.id)
        except Exception as e:
            logger.error(e)

    def _del_in_db(self):
        try:
            ScoreRecord.objects.filter(**self.dict(exclude={'course'}), course_id=self.course.id).delete()
        except Exception as e:
            logger.error(e)
