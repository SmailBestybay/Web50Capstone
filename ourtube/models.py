from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

    def __str__(self):
        return self.username

class YoutubeChannel(models.Model):
    pass

class Feed(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(User, through="Membership")
    channels = models.ManyToManyField(YoutubeChannel)

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    date_joined = models.DateField()
    is_owner = models.BooleanField()