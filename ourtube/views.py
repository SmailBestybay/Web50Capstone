from django.shortcuts import render, redirect
from django.http import HttpResponse
from .youtube_api_helper import get_videos, yt_search
from .models import YoutubeChannel as Ytc, Feed, User, Membership
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CreateFeedForm, JoinFeedForm
from datetime import datetime
from django.views.generic import TemplateView
from django.contrib import messages

class OurtubeTemplateView(TemplateView):

    template_name = 'ourtube/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feeds"] = get_feeds(self.request.user)
        context['create_form'] = CreateFeedForm()
        context['join_form'] = JoinFeedForm()
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class FeedView(OurtubeTemplateView):

    template_name = 'ourtube/feed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_feed = Feed.objects.get(id=self.kwargs['feed_id'])
        context['current_feed'] = current_feed

        channels = Ytc.objects.filter(feed__id=self.kwargs['feed_id'])
        for channel in channels:
            # set attributes dirrectly on objects
            channel.videos = get_videos(channel)
        context['channels'] = channels
        return context

class SearchView(OurtubeTemplateView):

    template_name = 'ourtube/search.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'search_channel' in request.GET.keys():
            if request.GET['search_channel'].strip() == '':
                messages.error(request, 'Search field must not be empty')
                return render(request, 'ourtube/search.html', context, status=400)
            results = yt_search(request.GET['search_channel'])
            context['results'] = results
        return render(request, self.template_name, context)
            

@login_required
def join_or_create_feed(request):
    if request.method != 'POST':
        return redirect('index')
    elif 'create_feed' in request.POST.keys():
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
        else:
            messages.error(request, 'Feed already exists')
            return redirect('index')
    elif 'join_feed' in request.POST.keys():
        form = JoinFeedForm(request.POST)
        if form.is_valid():
            current_user = User.objects.get(pk=request.user.id)
            feed_to_join = Feed.objects.get(pk=form.cleaned_data['feed_number'])
            try:
                Membership.objects.create(
                    user=current_user,
                    feed=feed_to_join,
                    date_joined = datetime.now(),
                    is_owner=False
                )
            except:
                messages.error(request, 'Already a member')
                return redirect('feed', feed_id=feed_to_join.id)
        return redirect('feed', feed_id=feed_to_join.id)
    return redirect('index')
        

def get_feeds(current_user):
    """ Get the feeds that current user owns or follows """
    return  Feed.objects.all().filter(members__id=current_user.id)
