from .models import Feed, User
from django import forms
from django.core import validators
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

class SearchForm(forms.Form):
    channel_name = forms.CharField(
        validators=[
            validators.MinLengthValidator(2),
            validators.MaxLengthValidator(128)
            ]
        )