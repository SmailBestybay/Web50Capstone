from .models import Feed
from django import forms

class CreateFeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = ['name']

class JoinFeedForm(forms.Form):
    feed_number = forms.IntegerField()