from ninja import Router

from upload.schemas import UploadDataSchema
from upload.util import extract_course_info_from_upload_data, update_course_statistics_result

router = Router(tags=["Upload"])


@router.post("/")
def upload_score_data(request, data: UploadDataSchema):
    # TODO change this two func call to background task
    extract_course_info_from_upload_data(data)
    update_course_statistics_result(data)

