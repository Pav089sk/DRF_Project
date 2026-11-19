from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import CustomUser


@shared_task
def block_inactive_users():
    cutoff = timezone.now() - timedelta(days=30)
    return CustomUser.objects.filter(last_login__isnull=False, last_login__lt=cutoff).update(is_active=False)
