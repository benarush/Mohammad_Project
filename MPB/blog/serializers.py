from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from .models import Post ,PostLikes
from django.utils import timezone
from django.contrib.auth.models import User
from .thirdPartyApplications.thirdParties import API

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        third_party_validation = API(validated_data['email'])
        if not third_party_validation.hunter_validation():
            raise serializers.ValidationError({"status": "unrecognized email by hunter.io ."},)
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        # Tuple of serialized model fields (see link [2])
        fields = ("id", "username", "password", "email")


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    date_posted = serializers.DateTimeField(default=timezone.now())
    class Meta:
        model = Post
        fields = ('id','title', 'content', 'date_posted', 'author_username',)

    def get_author_username(self, obj):
        return obj.author.username

    # def create(self, validated_data):
    #     pass


class PostLikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostLikes
        fields = "__all__"

    def create(self, validated_data):
        self.extra_validation(validated_data)
        return super().create(validated_data)

    @staticmethod
    def extra_validation(validated_data):
        if validated_data['post'].author == validated_data['user']:
            raise serializers.ValidationError({"status": "Cant like your own post"}, code=401)
        elif PostLikes.objects.filter(post=validated_data['post'], user=validated_data['user']):
            raise serializers.ValidationError({"status": "Already like this post..."}, code=401)
