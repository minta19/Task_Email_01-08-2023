from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
     

    def __str__(self) -> str:
        return self.username

class Blog(models.Model):
    title=models.CharField(max_length=255,unique=True)
    content=models.TextField()
    createdby=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='created_blog')
    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)
    blog_image=models.ImageField(upload_to='images/')

    def __str__(self) -> str:
        return f"{self.title} - {self.createdby} - {self.updated_time}"

class Comment(models.Model):
    comment_text=models.TextField(null=True,blank=True)
    blog_post=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='blog_comment')
    comment_createdby=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user_comment')
    comment_created_at=models.DateTimeField(auto_now_add=True)
    comment_updated_at=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.comment_text} - {self.blog_post} - {self.comment_updated_at}" 