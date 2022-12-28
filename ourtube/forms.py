from .models import Feed
from django.forms import ModelForm

class CreateFeedForm(ModelForm):
    class Meta:
        model = Feed
        fields = ['name']
