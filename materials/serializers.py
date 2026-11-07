from rest_framework import serializers
from materials.models import Course, Lesson, Subscription
from materials.validators import UrlValidator



class LessonSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Lesson
        validators = [UrlValidator(field='video_link')]
        fields = ['id', 'name', 'preview', 'description', 'video_link', 'course']


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=obj).exists()


    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description', 'lessons_count', 'lessons', 'is_subscribed']


class SubscriptSerializer(serializers.Serializer):

    class Meta:
        model = Subscription
        fields = ['user', 'course']

