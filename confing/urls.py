from django.contrib import admin
from django.urls import path, include, re_path
from .swagger import schema_view
from students.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/students/', StudentsAPIList.as_view()),
    path('api/v1/students/<int:pk>/', StudentsAPIUpdate.as_view()),
    path('api/v1/studentsdelete/<int:pk>/', StudentsAPIDestroy.as_view()),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/course/', CourseAPIView.as_view()),
    path('api/v1/course/<int:pk>/', CourseAPIUpdate.as_view()),
    path('api/v1/coursedelete/<int:pk>/', CourseAPIDestroy.as_view()),
    path('api/v1/comment/', CommentAPIView.as_view()),
    path('api/vi/comment/<int:pk>/', CommentAPIUpdateDestroy.as_view()),
    path('api/v1/rating/', RatingAPIView.as_view()), 
    path('api/v1/library/', LiteratureAPIView.as_view()),
    path('api/v1/library/<int:pk>/download/', DownloadBookView.as_view()),
    path('api/v1/forum/', MainPostAPIView.as_view()),
    path('api/v1/forum/subposts', SubPostAPIView.as_view()),
    path('api/v1/forum/subposts/<int:pk>/', SubPostAPIUpdateDestroy.as_view()),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

