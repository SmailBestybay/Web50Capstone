from django.shortcuts import render
from django.http import HttpResponse
from .youtube_api_helper import get_videos, search
from .models import YoutubeChannel as ytc

# Create your views here.
def index(request):
    
    
    return HttpResponse()