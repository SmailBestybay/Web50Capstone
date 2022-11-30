from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_likes(self):
        """ Get likes """
        return self.likes.all()
    
    def get_users_that_liked(self):
        """ Get a list of users that like the post"""
        users = []
        likes = self.likes.all()

        for like in list(likes):
            users.append(like.user)

        return users

    def __str__(self) -> str:
        return f"User: {self.user}, Short Content: {self.content[:20]}..."

class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.user} likes {self.post}"

class UserFollowing(models.Model):
    """ Don't forget to block from following the same user twice """

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    following_user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")

    def __str__(self) -> str:
        return f"{self.user} is following {self.following_user}"
    
    def is_valid_follow(self) -> bool:
        return self.user != self.following_user