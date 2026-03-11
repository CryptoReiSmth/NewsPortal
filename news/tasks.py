from datetime import timedelta

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

from .models import Post


@shared_task()
def subscribers_notification_task(**params):
    send_mail(**params)


@shared_task
def new_post_notification_task(subject, text_content, html_content, subscribers, from_email):
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task(ignore_result=True)
def weekly_newsletter():
    now = timezone.now()
    week_ago = now - timedelta(days=7)

    posts = (
        Post.objects.filter(time_in__gte=week_ago, time_in__lt=now)
        .prefetch_related('categories')
        .order_by('-time_in')
    )

    users = (
        User.objects.filter(categories__isnull=False)
        .exclude(email='')
        .distinct()
        .prefetch_related('categories')
    )

    for user in users:
        subscribed_categories = user.categories.all()

        user_posts = (
            posts.filter(categories__in=subscribed_categories)
            .distinct()
            .order_by('-time_in')
        )

        if not user_posts.exists():
            continue

        html_content = render_to_string(
            'news/weekly_newsletter.html',
            {
                'user': user,
                'posts': user_posts,
                'site_url': settings.SITE_URL,
            }
        )

        msg = EmailMultiAlternatives(
            subject='Свежие новости за неделю',
            body='За последнюю неделю появились новые публикации по вашим подпискам.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

