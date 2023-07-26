from rest_framework import serializers
from .models import CustomUser,Blog,Comment
class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['email','username','password']
        extra_kwargs={'password':{'write_only':True}}

    def create(self,validated_data):
        user=CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],

        )
            
        return user
    
class AdminSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['email','username','password']
        extra_kwargs={'password':{'write_only':True}}

    def create(self,validated_data):
        validated_data['is_staff'] = True
        validated_data['is_superuser'] = True

        user=CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            is_staff=True,
            is_superuser=True,
        )
            
        return user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['username']

class BlogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Blog
        fields=['title','content','blog_image']

class BlogListSerializer(serializers.ModelSerializer):
    createdby=UserSerializer(read_only=True)
    class Meta:
        model=Blog
        fields='__all__'


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model=Comment
        fields=['comment_text','blog_post']

class CommentListSerializer(serializers.ModelSerializer):
    comment_createdby=UserSerializer(read_only=True)

    class Meta:
        model=Comment
        fields='__all__'

class CommentEditSerializer(serializers.ModelSerializer):
    comment_createdby=UserSerializer(read_only=True)
    class Meta:
        model=Comment
        fields=['comment_text','comment_createdby']

class CommentforPostSerializer(serializers.ModelSerializer):
    comment_createdby=UserSerializer(read_only=True)

    class Meta:
        model=Comment
        fields=['comment_text','comment_createdby','comment_updated_at']


class BlogPostListSerializer(serializers.ModelSerializer):
    blog_comment=CommentforPostSerializer(many=True,read_only=True)
    createdby=UserSerializer(read_only=True)
    class Meta:
        model=Blog
        fields=['title','blog_image','content','createdby','updated_time','blog_comment']

