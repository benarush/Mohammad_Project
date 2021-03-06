from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    content = models.CharField(max_length=1000)
    date_posted = models.DateTimeField(default=timezone.now, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='post_like')

    def __str__(self):
        return f"<Post {self.title}>"

    @property
    def likes_count(self):
        return self.likes.count()

