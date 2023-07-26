from django.contrib import admin
from .models import Blog,Comment,CustomUser

admin.site.register(CustomUser)
admin.site.register(Blog)
admin.site.register(Comment)
