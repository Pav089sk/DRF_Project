from materials.serializers import CourseSerializer, LessonSerializer
from rest_framework import viewsets, generics, permissions
from materials.models import Course, Lesson
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.IsAuthenticated()]

        elif self.action =='retrieve':
            return [IsModerator | IsOwner]

        elif self.action == 'create':
            return [permissions.IsAuthenticated()]

        elif self.action in ['update', 'partial_update']:
            return [IsModerator | IsOwner]

        elif self.action == 'destroy':
            return [IsOwner]

        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = Course.objects.all()
        user = self.request.user

        if not user.groups.filter(name='moderators').exists():
            queryset = queryset.filter(owner=user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateApiView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonListApiView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Lesson.objects.all()
        user = self.request.user

        if not user.groups.filter(name='moderators').exists():
            queryset = queryset.filter(owner=user)

        return queryset


class LessonRetrieveApi(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateApiView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyApiView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [permissions.IsAdminUser | IsOwner]


