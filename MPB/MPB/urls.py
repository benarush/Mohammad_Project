from django.contrib import admin
from django.urls import path , include
from rest_framework.authtoken.views import obtain_auth_token
from rest_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="MPB Project")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('login/', obtain_auth_token, name="token-login"),
    path('overview/', schema_view),
]
