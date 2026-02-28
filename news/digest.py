from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Post


def send_weekly_digest():
    now = timezone.now()
    date_from = now - timedelta(days=7)

    weekly_posts = (
        Post.objects
        .filter(time_in__gte=date_from, time_in__lte=now)
        .prefetch_related("categories", "categories__subscribers")
        .order_by("-time_in")
    )

    user_posts_map: dict[int, dict[int, Post]] = {}

    for post in weekly_posts:
        subscribers = set()
        for cat in post.categories.all():
            for u in cat.subscribers.all():
                subscribers.add(u)

        for user in subscribers:
            user_posts_map.setdefault(user.id, {})
            user_posts_map[user.id][post.id] = post

    users = User.objects.filter(id__in=user_posts_map.keys()).only("id", "email", "username")
    for user in users:
        posts_for_user = list(user_posts_map[user.id].values())
        if not posts_for_user:
            continue

        subject = f"Новые статьи за неделю ({date_from:%d.%m.%Y} — {now:%d.%m.%Y})"

        html_content = render_to_string(
            "news/weekly_digest_email.html",
            {
                "user": user,
                "posts": posts_for_user,
                "site_url": getattr(settings, "SITE_URL", "http://127.0.0.1:8000"),
                "date_from": date_from.strftime("%d.%m.%Y"),
                "date_to": now.strftime("%d.%m.%Y"),
            },
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
