from ninja import Router
from ninja.security import django_auth

router = Router(tags=["Comment"])


@router.post("/{course_id:int}/", description="新建课程评论", auth=django_auth)
def create_comment(course_id: int):
    # TODO
    pass


@router.delete("/{comment_id:int}/", description="删除课程评论", auth=django_auth)
def delete_comment(course_id: int):
    # TODO
    pass


@router.get("/{course_id:int}/", description="获取课程评论")
def get_all_comments_of_course(course_id: int):
    # TODO
    pass
