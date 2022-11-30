from django.contrib import admin
from .models import User, Post, UserFollowing, Like

# Register your models here.
admin.site.register(User)
admin.site.register(UserFollowing)
admin.site.register(Like)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'timestamp')