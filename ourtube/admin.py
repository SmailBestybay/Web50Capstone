from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, YoutubeChannel, Feed, Membership


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1

class MemberUserAdmin(UserAdmin):
    inlines = (MembershipInline,)

class FeedAdmin(admin.ModelAdmin):
    inlines = (MembershipInline,)
# Register your models here.

admin.site.register(User, MemberUserAdmin)
admin.site.register(YoutubeChannel)
admin.site.register(Feed, FeedAdmin)
admin.site.register(Membership)