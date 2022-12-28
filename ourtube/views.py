from django.shortcuts import render, redirect
from django.http import HttpResponse
from .youtube_api_helper import get_videos, yt_search
from .models import YoutubeChannel as ytc, Feed, User, Membership
from django.contrib.auth.decorators import login_required
from .forms import CreateFeedForm
from datetime import datetime

@login_required
def index(request):
    
    context = {}
    context["feeds"] = get_feeds()
    context['form'] = CreateFeedForm()
    
    return render(request, 'ourtube/index.html', context)

@login_required
def feed(request, feed_id):
    context = {}
    context['feeds'] = get_feeds()
    context['form'] = CreateFeedForm()

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
    context['form'] = CreateFeedForm()

    if request.method == 'POST':
        if request.POST['search_channel'].strip() == '':
            context['message'] = 'Post must not be empty'
            return render(request, 'ourtube/search.html', context, status=400)
        results = yt_search(request.POST['search_channel'])
        context['results'] = results

    return render(request, 'ourtube/search.html', context)

@login_required
def join_or_create_feed(request):
    if request.method != 'POST':
        return redirect('index')
    elif request.POST['create_feed']:
        form = CreateFeedForm(request.POST)
        if form.is_valid():
            current_user = User.objects.get(pk=request.user.id)
            new_feed = Feed.objects.create(name=form.cleaned_data['name'])
            Membership.objects.create(
                user=current_user,
                feed=new_feed,
                date_joined = datetime.now(),
                is_owner=True
                )
            return redirect('feed', feed_id=new_feed.id)
    # elif request.POST['join_feed']:
    #     return redirect('feed', feed_id=0)
    return redirect('index')
        

def get_feeds():
    return  Feed.objects.all()
