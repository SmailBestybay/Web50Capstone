from django.shortcuts import render
from django.http import HttpResponse
from .youtube_api_helper import get_videos, yt_search
from .models import YoutubeChannel as ytc, Feed, User
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    
    context = {}
    context["feeds"] = get_feeds()
    
    return render(request, 'ourtube/index.html', context)

@login_required
def feed(request, feed_id):
    context = {}
    context['feeds'] = get_feeds()

    current_feed = Feed.objects.get(id=feed_id)
    context['current_feed'] = current_feed

    channels = ytc.objects.filter(feed__id=feed_id)
    for channel in channels:
        # set attributes dirrectly on objects
        channel.videos = get_videos(channel)
    context['channels'] = channels

    return render(request, 'ourtube/feed.html', context)

@login_required
def search_view(request):
    
    context = {}
    context["feeds"] = get_feeds()

    if request.method == 'POST':
        if request.POST['search_channel'].strip() == '':
            context['message'] = 'Post must not be empty'
            return render(request, 'ourtube/search.html', context, status=400)
        results = yt_search(request.POST['search_channel'])
        context['results'] = results

    return render(request, 'ourtube/search.html', context)


def get_feeds():
    return  Feed.objects.all()
