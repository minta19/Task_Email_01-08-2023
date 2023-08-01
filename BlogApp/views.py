from django.shortcuts import render
from .models import CustomUser,Blog,Comment
from .serializers import (SignupSerializer,AdminSignupSerializer,BlogCreateSerializer,BlogListSerializer
                          ,CommentCreateSerializer,CommentListSerializer,CommentEditSerializer,BlogPostListSerializer)
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from django.template.loader import get_template
#Normal user signup
class Signup(APIView):
    
  def post(self,request):
    serializer=SignupSerializer(data=request.data)
    if serializer.is_valid():
      user=serializer.save()

      subject='WELCOME TO BLOG PLATFORM'
      from_email=settings.DEFAULT_FROM_EMAIL
      receiptant_list=[user.email]
      ctx={'username':user.username}
      message=get_template('email.html').render(ctx)
      email=EmailMessage(subject,message,from_email,receiptant_list)
      email.content_subtype="html"
      email.send()
            
                
      return Response({'MESSAGE':'USER CREATED'},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  

#Admin User signup
class AdminSignUp(APIView):
  permission_classes=[IsAdminUser,IsAuthenticated]
  def post(self,request):
    serializer=AdminSignupSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response({'MESSAGE':'ADMIN USER CREATED'},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  
#blog creation
class BlogCreate(generics.CreateAPIView):
  permission_classes=[IsAuthenticated]
  queryset=Blog.objects.all()
  authentication_classes=[JWTAuthentication]
  serializer_class=BlogCreateSerializer

  def perform_create(self, serializer):
    user=self.request.user
    serializer.save(createdby=user)

    if serializer.is_valid():

      subject='YOUR BLOG CREATED'
      from_email=settings.DEFAULT_FROM_EMAIL
      receiptant_list=[user.email]
      ctx={'username':user.username,'title': serializer.data['title'],'new_blog':serializer.instance}
      message=get_template('blogemail.html').render(ctx)

      new_blog=serializer.instance
      email=EmailMessage(subject,message,from_email,receiptant_list)
      if new_blog.blog_image:
        email.attach(new_blog.blog_image.name,new_blog.blog_image.read(),('image/*'))
      email.content_subtype="html"
      email.send()
            
  
  def post(self, request, *args, **kwargs):
    response= super().post(request, *args, **kwargs)
    return Response({"MESSAGE":"BLOG CREATED"})

#only blog feed of user 
class BlogList(generics.ListAPIView):
  permission_classes=[IsAuthenticated]
  queryset=Blog.objects.all()
  authentication_classes=[JWTAuthentication]
  serializer_class=BlogListSerializer

#blog can be edited only by the owner
class Blog_edit(generics.RetrieveUpdateDestroyAPIView):
  permission_classes=[IsAuthenticated]
  queryset=Blog.objects.all()
  authentication_classes=[JWTAuthentication]
  serializer_class=BlogListSerializer
  
  def perform_update(self, serializer):
    blog=self.get_object()
    if blog.createdby != self.request.user:
      raise PermissionDenied("YOU ARE NOT ALLOWED TO PERFORM THIS ACTION")
    return super().perform_update(serializer)
  
  def perform_destroy(self, instance):
    if instance.createdby != self.request.user:
      raise PermissionDenied("YOU ARE NOT ALLOWED TO PERFORM THIS ACTION")
    return super().perform_destroy(instance)
  
  def delete(self, request, *args, **kwargs):
    response= super().delete(request, *args, **kwargs)
    return Response({"MESSAGE":"BLOG DELETED"})
  
#comment creation by user
class CommentCreate(generics.CreateAPIView):
  permission_classes=[IsAuthenticated]
  authentication_classes=[JWTAuthentication]
  serializer_class=CommentCreateSerializer
  
  def perform_create(self, serializer):
    serializer.save(comment_createdby=self.request.user)

  def post(self, request, *args, **kwargs):
    response= super().post(request, *args, **kwargs)
    comment_data=response.data
    return Response({"MESSAGE":"COMMENT ADDED","COMMENT":comment_data})

 #list of comment only 
class CommentList(generics.ListAPIView):
  permission_classes=[IsAuthenticated]
  authentication_classes=[JWTAuthentication]
  serializer_class=CommentListSerializer
  queryset=Comment.objects.all()

 #comment edit by owner 
class CommentEdit(generics.RetrieveUpdateDestroyAPIView):
  permission_classes=[IsAuthenticated]
  authentication_classes=[JWTAuthentication]
  serializer_class=CommentEditSerializer
  queryset=Comment.objects.all()

  def perform_update(self, serializer):
    comment=self.get_object()
    if comment.comment_createdby != self.request.user:
      raise PermissionDenied("YOU ARE NOT ALLOWED TO PERFORM THIS ACTION")
    return super().perform_update(serializer)
  
  def perform_destroy(self, instance):
    if instance.comment_createdby != self.request.user:
      raise PermissionDenied("YOU ARE NOT ALLOWED TO PERFORM THIS ACTION")
    return super().perform_destroy(instance)
  
  def delete(self, request, *args, **kwargs):
    response= super().delete(request, *args, **kwargs)
    return Response({"MESSAGE":"COMMENT DELETED"})

 #Blog lists for admin 
class AdminBlogList(generics.ListAPIView):
  permission_classes=[IsAdminUser,IsAuthenticated]
  queryset=Blog.objects.all()
  authentication_classes=[JWTAuthentication]
  serializer_class=BlogListSerializer

#blog detail and delete option for admin
class AdminBlogEdit(generics.RetrieveDestroyAPIView):
  permission_classes=[IsAdminUser,IsAuthenticated]
  queryset=Blog.objects.all()
  authentication_classes=[JWTAuthentication]
  serializer_class=BlogListSerializer

  def delete(self, request, *args, **kwargs):
    response= super().delete(request, *args, **kwargs)
    return Response({"MESSAGE":"BLOG DELETED BY ADMIN"})

#comment list for admin
class AdminCommentList(generics.ListAPIView):
  permission_classes=[IsAuthenticated,IsAdminUser]
  queryset=Comment.objects.all()
  authentication_classes=[JWTAuthentication]
  serializer_class=CommentListSerializer

#comment details and delete options for admin
class AdminCommentEdit(generics.RetrieveDestroyAPIView):
  permission_classes=[IsAdminUser,IsAuthenticated]
  queryset=Comment.objects.all()
  authentication_classes=[JWTAuthentication]
  serializer_class=CommentListSerializer

  def delete(self, request, *args, **kwargs):
    response= super().delete(request, *args, **kwargs)
    return Response({"MESSAGE":"comment DELETED BY ADMIN"})


#list view of post with their comments
class BlogPostList(generics.ListAPIView):
  permission_classes=[IsAuthenticated]
  queryset=Blog.objects.all()
  authentication_classes=[JWTAuthentication]
  serializer_class=BlogPostListSerializer

