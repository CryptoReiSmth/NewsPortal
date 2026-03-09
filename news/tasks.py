from celery import shared_task
from django.core.mail import send_mail


@shared_task()
def subscribers_notification_task(**params):
    send_mail(**params)
