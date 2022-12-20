from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, YoutubeChannel, Feed, Membership

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(YoutubeChannel)
admin.site.register(Feed)
admin.site.register(Membership)