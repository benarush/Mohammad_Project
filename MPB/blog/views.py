from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from .serializers import *
from rest_framework import permissions
from .models import *
from django.conf import settings

@receiver(post_save , sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



class CreateUserView(CreateAPIView):

    model = User()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer


class CreatePostView(CreateAPIView):
    model = Post
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


#    I could do it more elegant by using API Class based view ,
#    but only for the test i want to show more of my abilities
@api_view(['POST'])
@authentication_classes([TokenAuthentication,])
def create_post_likes(request):
    query_dict_data = request.data.copy()
    query_dict_data['user'] = request.auth.user.id
    serializer = PostLikesSerializer(data=query_dict_data, many=False)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)
    return Response({"status": "failed"}, status=405)

