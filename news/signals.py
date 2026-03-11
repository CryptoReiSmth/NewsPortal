from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string

from .models import Category, Post
from .tasks import subscribers_notification_task, new_post_notification_task


@receiver(m2m_changed, sender=Category.subscribers.through)
def subscribers_notification(sender, instance, action, pk_set, **kwargs):
    user = User.objects.get(pk__in=pk_set)
    username = user.username
    email = user.email
    name = instance.name

    if action == 'post_add':
        params = {
            'subject': 'Новая подписка',
            'message': f'Привет, {username}! Вы подписались категорию {name}! '
                       f'Список категорий ваших подписок: {", ".join(cat.name for cat in user.categories.all())}',
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'recipient_list': [email]
        }
        subscribers_notification_task.delay(**params)

    if action == 'post_remove':
        params = {
            'subject': 'Отписка от категории',
            'message': f'Привет, {username}! Вы отписались от категории {name}! '
                       f'Список категорий ваших подписок: {", ".join(cat.name for cat in user.categories.all())}',
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'recipient_list': [email]
        }
        subscribers_notification_task.delay(**params)

@receiver(m2m_changed, sender=Category.subscribers.through)
def subscribers_notification(sender, instance, action, pk_set, **kwargs):
    if action in ('post_add', 'post_remove') and pk_set:
        for user_pk in pk_set:
            subscribers_notification_task.delay(user_pk, instance.pk, action)


@receiver(m2m_changed, sender=Post.categories.through)
def notify_about_new_post(sender, instance, action, **kwargs):
    if action != 'post_add' or not instance.pk:
        return

    subscribers = list(
        instance.categories.all()
        .values_list('subscribers__email', flat=True)
        .exclude(subscribers__email='')
        .distinct()
    )

    if not subscribers:
        return

    text_content = instance.preview()
    html_content = render_to_string(
        'news/post_created_email.html',
        {
            'text': text_content,
            'link': f'{settings.SITE_URL}{instance.get_absolute_url()}',
        },
    )

    new_post_notification_task.delay(
        instance.title,
        text_content,
        html_content,
        subscribers,
        settings.DEFAULT_FROM_EMAIL,
    )
