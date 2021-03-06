from django.contrib import admin
from .models import *

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ("title", "content", "date_posted", "author", "likes")
    list_display = ("id", "title", "content", "date_posted", "author", "likes_count")

    def likes_count(self, obj):
        return "\n" + str(obj.likes.count())

