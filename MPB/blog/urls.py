from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from blog.views import *

urlpatterns = [
    path('create_user/', CreateUserView.as_view(), name="create-user"),
 #   path('create_post/', CreatePostView.as_view(), name="create-user"),
    path('post_like/', create_post_likes, name="create_post_likes"),
    path("postAPI/", PostAPIView.as_view(), name="post-api"),

]
