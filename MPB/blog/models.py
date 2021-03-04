from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class UserDetails(models.Model):
    full_name = models.CharField(max_length=150, blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"<{self.title}>"

    @property
    def likes_count(self):
        return PostLikes.objects.filter(post=self).count()


class PostLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post}"
