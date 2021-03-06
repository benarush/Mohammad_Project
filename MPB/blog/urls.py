from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings

from blog.views import *

urlpatterns = [
    path('create_user/', CreateUserView.as_view(), name="create-user"),
    path('post_like/', create_post_likes, name="create_post_likes"),
    path("postAPI/", PostAPIView.as_view(), name="post-api"),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
