from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string

from .models import Category, PostCategory


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
