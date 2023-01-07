import os

from qinglianjie_ninja import settings


def user_directory_path(instance, filename):
    ext = filename.split('.').pop()
    name = filename.split('.')[-2]
    filename = '{0}_{1}.{2}'.format(instance.user.username, name, ext)
    return os.path.join("profile", "avatar", filename)