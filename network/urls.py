
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("update_post/<int:post_id>", views.update_post, name="update_post"),
    path("profile/<str:username>/", views.profile_view, name="profile"),
    path("following", views.following, name="following"),
    path("follow_unfollow", views.follow_unfollow, name="follow_unfollow"),
    path("like_unlike", views.like_unlike, name="like_unlike")
]
