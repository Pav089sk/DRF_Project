from rest_framework.test import APITestCase
from django.contrib.auth.models import Group
from materials.models import Course, Lesson, Subscription
from users.models import CustomUser


class LessonTestCase(APITestCase):
    def setUp(self):
        self.owner = CustomUser.objects.create_user(
            email='owner@owner.com',
            password='test12345'
        )
        self.moderator = CustomUser.objects.create_user(
            email='moderator@moderator.com',
            password='test12345'
        )
        self.stranger = CustomUser.objects.create_user(
            email='stranger@stranger.com',
            password='test12345'
        )
        group, created = Group.objects.get_or_create(name='moderators')
        self.moderator.groups.add(group)

        self.course = Course.objects.create(
            name='Тестовый курс',
            description='Курс для тестов',
            owner=self.owner
        )
        self.lesson_1 = Lesson.objects.create(
            name='Урок 1',
            description='Первый тестовый урок',
            course=self.course,
            owner=self.owner
        )
        self.lesson_2 = Lesson.objects.create(
            name='Урок 2',
            description='Второй тестовый урок',
            course=self.course,
            owner=self.owner
        )

    def test_setup_check(self):
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(CustomUser.objects.count(), 3)

    def test_create_lesson_by_owner(self):
        self.client.force_authenticate(user=self.owner)
        data = {"name":"Урок 3", "description":"Третий тестовый урок", "course": self.course.id}
        response = self.client.post('/api/materials/lesson/create/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Lesson.objects.count(), 3)

    def test_delete_lesson_by_stranger(self):
        self.client.force_authenticate(user=self.stranger)
        response = self.client.delete(f'/api/materials/lesson/del/{self.lesson_1.id}/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_moderator_update_and_delete_lessons(self):
        self.client.force_authenticate(user=self.moderator)
        update_data = {"name": "Обновлённый урок модератора", "description": "Теперь его трогал модератор"}
        response_patch = self.client.patch(f'/api/materials/lesson/upd/{self.lesson_1.id}/', update_data)
        self.assertEqual(response_patch.status_code, 200)
        updated_lesson = Lesson.objects.get(id=self.lesson_1.id)
        self.assertEqual(updated_lesson.name, "Обновлённый урок модератора")
        response_delete = self.client.delete(f'/api/materials/lesson/del/{self.lesson_1.id}/')
        self.assertEqual(response_delete.status_code, 403)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_anonymous_cannot_create_lesson(self):
        data = {
            "name": "Урок для анонимов",
            "description": "Не должен создаться",
            "course": self.course.id,
        }
        response = self.client.post('/api/materials/lesson/create/', data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_subscription_toggle(self):
        self.client.force_authenticate(user=self.stranger)
        response_1 = self.client.post('/api/materials/subscriptions/', {"course": self.course.id})
        self.assertEqual(Subscription.objects.filter(user=self.stranger, course=self.course).count(), 1)
        response_2 = self.client.post('/api/materials/subscriptions/', {"course": self.course.id})
        self.assertEqual(Subscription.objects.count(), 0)



