from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import m2m_changed

from .models import Category


@receiver(m2m_changed, sender=Category.subscribers.through)
def subscribers_notification(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        user = User.objects.get(pk__in=pk_set)
        send_mail(
            subject='Новая подписка',
            message=f'Привет, {user.username}! Вы подписались на категорию {instance.name}! \
            \nСписок ваших подписок: {", ".join(cat.name for cat in user.categories.all())}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
    elif action == 'post_remove':
        user = User.objects.get(pk__in=pk_set)
        send_mail(
            subject='Отписка',
            message=f'Привет, {user.username}! Вы отписались от категории {instance.name}! \
            \nСписок ваших подписок: {", ".join(cat.name for cat in user.categories.all())}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
