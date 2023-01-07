"""qinglianjie_ninja URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from ninja import NinjaAPI

from qinglianjie_auth.api import router as qinglianjie_auth_router
from qinglianjie_ninja import settings
from upload.api import router as upload_router
from course.api import router as course_router
from comment.api import router as comment_router
from user.api import router as user_router


api = NinjaAPI(csrf=True)

api.add_router("/auth/", qinglianjie_auth_router)
api.add_router("/upload/", upload_router)
api.add_router("/course/", course_router)
api.add_router("/comment/", comment_router)
api.add_router("/user/", user_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
