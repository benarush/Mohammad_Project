from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, schema
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from rest_framework import permissions
from .models import *
from django.conf import settings
from rest_framework.schemas import AutoSchema
import coreapi


class PostListAPISchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if 'post_like' in path:
            extra_fields = [coreapi.Field('post'),]
        elif method.lower() in ['post', 'put']:
            extra_fields = self.post_update_fields(method.lower())
        elif method.lower() == 'delete':
            extra_fields = self.delete_fields

        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields

    def post_update_fields(self, method):
        extra_fields = [coreapi.Field('title'),coreapi.Field('content')]
        return extra_fields if method == 'post' else extra_fields + [coreapi.Field('post_id'), ]

    @property
    def delete_fields(self):
        return [coreapi.Field('post_id',
                                          location="body",
                                          type="string",
                                          description='{"post_id":"number"}',
                                          example={"post_id":"number"}
            ),]


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class CreateUserView(CreateAPIView):
    """
    Create User Account
    """
    model = User()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class PostAPIView(APIView):
    """
    Retrieve, update or delete a post instance.
    """
    schema = PostListAPISchema()
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        all_posts_data_two_queries = Post.objects.all().select_related('author').prefetch_related('likes')
        serializer = PostSerializer(all_posts_data_two_queries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)
        return Response(serializer._errors, status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, format=None):
        pk = request.data.get("post_id", None)
        if not pk:
            return Response("Bad Request, need to provide post_id.", status=status.HTTP_400_BAD_REQUEST)
        post = get_object_or_404(Post, id=pk)
        if post.author != request.user:
            return Response("permission denied", status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        pk = request.data.get("post_id", None)
        if not pk:
            return Response("Bad Request, need to provide post_id.", status=status.HTTP_400_BAD_REQUEST)
        post = get_object_or_404(Post, id=pk)
        if post.author != request.user:
            return Response("permission denied", status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@authentication_classes([TokenAuthentication,])
@schema(PostListAPISchema())
def create_post_likes(request):
    """
    Create Post Like
    """
    post = get_object_or_404(Post, id=request.data.get("post", None))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)
