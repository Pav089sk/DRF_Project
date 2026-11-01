from materials.serializers import CourseSerializer, LessonSerializer
from rest_framework import viewsets, generics, permissions
from materials.models import Course, Lesson
from users.permissions import IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsModerator()]

        elif self.action in ['create', 'destroy']:
            return [permissions.IsAdminUser()]

        elif self.action in ['update', 'partial_update']:
            return [IsModerator()]

        return [permissions.IsAuthenticated()]


class LessonCreateApiView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAdminUser]

class LessonListApiView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator]

class LessonRetrieveApi(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator]

class LessonUpdateApiView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator]

class LessonDestroyApiView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [permissions.IsAdminUser]

