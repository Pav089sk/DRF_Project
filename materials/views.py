from django.shortcuts import render
from materials.serializers import CourseSerializer, LessonSerializer
from rest_framework import viewsets, generics
from materials.models import Course, Lesson



class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonCreateApiView(generics.CreateAPIView):
    serializer_class = LessonSerializer


class LessonListApiView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonRetrieveApi(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateApiView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonDestroyApiView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()

