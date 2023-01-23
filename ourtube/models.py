from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import UniqueConstraint

class User(AbstractUser):
    pass

    def __str__(self):
        return self.username

class YoutubeChannel(models.Model): 
    name = models.CharField(max_length=128)
    channel_id = models.CharField(max_length=128, unique=True)
    playlist_id = models.CharField(max_length=128, unique=True)

    def __str__(self) -> str:
        return self.name

class Feed(models.Model):
    name = models.CharField(max_length=128, unique=True)
    members = models.ManyToManyField(User, through="Membership")
    channels = models.ManyToManyField(YoutubeChannel, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    date_joined = models.DateField()
    is_owner = models.BooleanField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'feed'], name='unique_members'),
        ]