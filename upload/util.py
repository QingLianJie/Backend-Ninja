from typing import List, Dict

from django.db import transaction

from course.models import CourseInfo, CourseStatisticsResult
from course.schemas import CourseInfoSchema
from score.schemas import ScoreRecordSchema
from score.util import select_by_heu_username_hash
from upload import logger
from upload.schemas import UploadDataSchema


def extract_course_info_from_upload_data(data: UploadDataSchema):
    for score_record in data.scores:
        with transaction.atomic():
            course: CourseInfoSchema = CourseInfoSchema(**score_record.dict())
            try:
                # Try to create course in db
                course_in_db = CourseInfo.objects.create(**course.dict())
                course_in_db.save()
                # Try to create course statistics in db
                course_statistics_in_db = CourseStatisticsResult.objects.create(course=course_in_db)
                course_statistics_in_db.save()
                logger.info(f"Course {course} created.")
            except Exception as e:
                logger.error(e)


def update_course_statistics_result(data: UploadDataSchema):
    # Undo previous course statistic update
    pre_records = select_by_heu_username_hash(data.heu_username_hash)
    for record in pre_records:
        record.update_statistics(undo=True)

    # Update course statistic
    new_records: List[ScoreRecordSchema] = [
        ScoreRecordSchema.from_raw_score_content(data.heu_username_hash, x) for x in data.scores]
    for record in new_records:
        record.update_statistics(undo=False)
