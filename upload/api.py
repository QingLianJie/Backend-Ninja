from django.contrib.auth.models import User
from ninja import Router
from ninja.security import django_auth

from upload.schemas import UploadDataSchema
from upload.util import extract_course_info_from_upload_data, update_course_statistics_result

router = Router(tags=["Upload"])


@router.post("/", auth=django_auth)
def upload_score_data(request, data: UploadDataSchema):
    user: User = request.user
    # TODO change this two func call to background task
    extract_course_info_from_upload_data(data)
    update_course_statistics_result(data, user.id)

