from materials.serializers import CourseSerializer, LessonSerializer
from rest_framework import viewsets, generics
from materials.models import Course, Lesson, Subscription
from users.permissions import IsModerator, IsOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]

        elif self.action =='retrieve':
            permission_classes = [IsModerator | IsOwner]

        elif self.action == 'create':
            permission_classes = [~IsModerator & IsAuthenticated]

        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsModerator | IsOwner]

        elif self.action == 'destroy':
            permission_classes = [IsOwner & ~IsModerator ]

        return [permission() for permission in permission_classes]

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
    permission_classes = [IsAuthenticated & ~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonListApiView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsOwner]  # Пускаем только владельцев

    def perform_destroy(self, instance):
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            raise PermissionDenied("Модераторы не могут удалять уроки.")
        instance.delete()


class SubscriptApiView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'
        return Response({"message": message})