from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="author_profile")
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts = self.posts.all()
        posts_rating = sum(p.rating for p in posts) * 3

        user_comments = self.user.comments.all()
        user_comments_rating = sum(c.rating for c in user_comments)

        post_comments_rating = 0
        for p in posts:
            post_comments_rating += sum(c.rating for c in p.comments.all())

        self.rating = posts_rating + user_comments_rating + post_comments_rating
        self.save(update_fields=['rating'])


class Category(models.Model):
    name = models.CharField(max_length=64, default='No category', unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    news = 'N'
    article = 'A'
    TYPES = [(news, 'Новость'), (article, 'Статья')]
    type = models.CharField(max_length=1, choices=TYPES, default=news)
    time_in = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='posts')
    categories = models.ManyToManyField('Category', through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
