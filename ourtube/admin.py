from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, YoutubeChannel, Feed, Membership


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1

class YoutubeChannelInline(admin.TabularInline):
    model = Feed.channels.through
    extra = 1

class MemberUserAdmin(UserAdmin):
    '''extend UserAdmin to add membership inline to admin page'''
    inlines = (MembershipInline,)

class FeedAdmin(admin.ModelAdmin):
    inlines = (MembershipInline, YoutubeChannelInline)
# Register your models here.

admin.site.register(User, MemberUserAdmin)
admin.site.register(YoutubeChannel)
admin.site.register(Feed, FeedAdmin)
# don't need to register membership model with admin because inlines serve that need.
# admin.site.register(Membership)