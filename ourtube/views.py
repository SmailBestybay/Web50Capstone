from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from datetime import datetime
from .models import YoutubeChannel as Ytc, Feed, User, Membership
from .forms import CreateFeedForm, JoinFeedForm, CustomUserCreationFrom, SearchForm
from .helper import get_videos, yt_search, get_feeds

class OurtubeTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'ourtube/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feeds"] = get_feeds(self.request.user)
        context['create_form'] = CreateFeedForm()
        context['join_form'] = JoinFeedForm()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if 'create_feed' in request.POST.keys():
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
                context['create_form'] = form
                return self.render_to_response(context)

        if 'join_feed' in request.POST.keys():
            form = JoinFeedForm(request.POST)
            if form.is_valid():
                current_user = User.objects.get(pk=request.user.id)
                feed_to_join = get_object_or_404(Feed, pk=form.cleaned_data['feed_number'])
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
            else:
                context['join_form'] = form
                return self.render_to_response(context)

        return self.render_to_response(context)

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
        form = SearchForm()
        context['form'] = form
        if 'channel_name' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                results = yt_search(form.cleaned_data['channel_name'])
                context['results'] = results
            else:
                context['form'] = form
                return render(request, 'ourtube/search.html', context, status=400)
        return render(request, self.template_name, context)

class SignUpView(CreateView):
    form_class = CustomUserCreationFrom
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"
