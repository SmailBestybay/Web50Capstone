from .models import Feed, User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class CreateFeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = ['name']

class JoinFeedForm(forms.Form):
    feed_number = forms.IntegerField()

class CustomUserCreationFrom(UserCreationForm):
    """ Extends UserCreationForm to work with User """

    class Meta(UserCreationForm.Meta):
        model = User
