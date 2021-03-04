from django.contrib import admin
from .models import *

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Post._meta.get_fields() if f.one_to_many != True]


@admin.register(PostLikes)
class PostLikesAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PostLikes._meta.get_fields() if f.one_to_many != True]


@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in UserDetails._meta.get_fields() if f.one_to_many != True]