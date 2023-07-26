from django.urls import path
from .views import (Signup,AdminSignUp,BlogCreate,BlogList,CommentCreate,CommentList,Blog_edit,
                    CommentEdit,AdminBlogList,BlogPostList,AdminBlogEdit,AdminCommentEdit,AdminCommentList)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns=[
    path('api/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/token/refresh',TokenRefreshView.as_view(),name='token_refresh'),
    path('signup/',Signup.as_view(),name='user_signup'),
    path('adminsignup/',AdminSignUp.as_view(),name='admin_signup'),
    path('create/',BlogCreate.as_view(),name='blog_create'),
    path('list/',BlogList.as_view(),name='blog_list'),
    path('commentcreate/',CommentCreate.as_view(),name='comment_create'),
    path('commentlist/',CommentList.as_view(),name='comment_list'),
    path('edit/<int:pk>',Blog_edit.as_view(),name='blog_edit'),
    path('commentedit/<int:pk>',CommentEdit.as_view(),name='comment_edit'),
    path('admin/bloglist/',AdminBlogList.as_view(),name='admin_blog_list'),
    path('admin/blogedit/<int:pk>/',AdminBlogEdit.as_view(),name='admin_blog_edit'),
    path('admin/commentlist/',AdminCommentList.as_view(),name='admin_comment_list'),
    path('admin/commentedit/<int:pk>/',AdminCommentEdit.as_view(),name='admin_comment_edit'),
    path('blogwithcomment/',BlogPostList.as_view(),name='blog_comment')

    
]