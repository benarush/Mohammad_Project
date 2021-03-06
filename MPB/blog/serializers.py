from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from .models import Post
from django.utils import timezone
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        #raise serializers.ValidationError({"status": "unrecognized email by hunter.io ."},)
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ("id", "username", "password", "email")


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    date_posted = serializers.DateTimeField(default=timezone.now())
    numbers_of_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id','title', 'content', 'date_posted', 'author_username','numbers_of_likes')

    def get_numbers_of_likes(self, obj):
        return obj.likes.count()

    def get_author_username(self, obj):
        return obj.author.username

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

    # def create(self, validated_data):
    #     pass


# class PostLikesSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = PostLikes
#         fields = "__all__"
#
#     def create(self, validated_data):
#         self.extra_validation(validated_data)
#         return super().create(validated_data)
#
#     @staticmethod
#     def extra_validation(validated_data):
#         if validated_data['post'].author == validated_data['user']:
#             raise serializers.ValidationError({"status": "Cant like your own post"}, code=401)
#         elif PostLikes.objects.filter(post=validated_data['post'], user=validated_data['user']):
#             raise serializers.ValidationError({"status": "Already like this post..."}, code=401)
