from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string

from .models import Category, PostCategory
from .tasks import subscribers_notification_task


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


def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'news/post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, action, **kwargs):
    if action == 'post_add':
        categories = instance.categories.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]
        subscribers_emails = list(set(subscribers_emails))

        if subscribers_emails:
            send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)
