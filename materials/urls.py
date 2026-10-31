from django.urls import path, include
from rest_framework.routers import DefaultRouter
from materials.views import CourseViewSet, LessonCreateApiView, LessonListApiView, LessonRetrieveApi, LessonUpdateApiView, LessonDestroyApiView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
    path('lesson/create/',LessonCreateApiView.as_view(), name='lesson-create'),
    path('lesson/list/', LessonListApiView.as_view(), name='lessons-list'),
    path('lesson/<int:pk>/', LessonRetrieveApi.as_view(), name='lesson-get'),
    path('lesson/upd/<int:pk>/', LessonUpdateApiView.as_view(), name='lesson-update'),
    path('lesson/del/<int:pk>/', LessonDestroyApiView.as_view(), name='lesson-delete'),
]