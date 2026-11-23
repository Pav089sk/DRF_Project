from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from materials.models import Course, Subscription



@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(pk=course_id)
    emails = (
        Subscription.objects
        .filter(course=course)
        .select_related('user')
        .values_list('user__email', flat=True)
    )
    if emails:
        send_mail(
            subject=f'Обновление курса: {course.name}',
            message=f'Курс «{course.name}» был обновлён. Загляните, что изменилось!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=list(emails),
            fail_silently=False,
        )



