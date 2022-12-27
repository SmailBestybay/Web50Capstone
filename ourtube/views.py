from django.shortcuts import render
from django.http import HttpResponse
from .youtube_api_helper import get_videos
from .models import YoutubeChannel as ytc

# Create your views here.
def index(request):
    kenji = ytc.objects.get(pk=1)
    context = {
        kenji.name : kenji.channel_id
    }
    r = get_videos(kenji)

    context['yt'] = r
    
    return HttpResponse(context.items())