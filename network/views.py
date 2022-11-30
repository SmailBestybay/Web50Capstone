from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .models import User, Post, UserFollowing, Like
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

def index_view(request):

    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10) # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'posts' : posts, 'page_obj' : page_obj}


    if request.method == 'POST':
        if request.POST['content'].strip() == '':
            context['message'] = 'Post must not be empty'
            return render(request, 'network/index.html', context, status=400)
        
        new_post = Post(
            user=request.user,
            content=request.POST['content']
        )
        new_post.save()

        return render(request, 'network/index.html', context)
            
    return render(request, 'network/index.html', context)

@login_required
def following(request):
    user = get_object_or_404(User, pk=request.user.id)
    
    following = user.following.all()

    users = []

    for item in following:
        users.append(item.following_user)

    posts = Post.objects.filter(user__in=users).order_by('-timestamp')
    paginator = Paginator(posts, 10) # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'posts' : posts, 'page_obj' : page_obj}


    if request.method == 'POST':
        if request.POST['content'].strip() == '':
            context['message'] = 'Post must not be empty'
            return render(request, 'network/index.html', context, status=400)
        
        new_post = Post(
            user=request.user,
            content=request.POST['content']
        )
        new_post.save()

        return render(request, 'network/index.html', context)
            
    return render(request, 'network/index.html', context)

def profile_view(request, username):

    profile_owner = User.objects.get(username=username)
    followers = profile_owner.followers.all() # need all to find if to follow or not
    following = profile_owner.following.count()

    

    posts = Post.objects.all().filter(user=profile_owner).order_by('-timestamp')
    paginator = Paginator(posts, 10) # Show 10 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'posts' : posts,
                'page_obj' : page_obj,
                'followers': followers,
                'following': following,
                'user_profile': profile_owner
            }

    if request.user.is_authenticated:
        follower = User.objects.get(pk=request.user.id)
        is_following = followers.filter(user=follower).exists()
        context['is_following'] = is_following

    return render(request, 'network/profile.html', context)

@login_required
def follow_unfollow(request):

    if request.method != "POST":
        return JsonResponse({'error': 'Only Post method allowed on this path'}, status=400)
    # need user and following_user
    user = User.objects.get(pk=request.user.id)

    if request.method == "POST":
        if 'follow' in request.POST:
            user_to_follow = User.objects.get(username=request.POST["follow"])
            UserFollowing(user=user, following_user=user_to_follow).save()
            return redirect('profile', username=user_to_follow.username)

        if 'unfollow' in request.POST:
            user_to_follow = User.objects.get(username=request.POST["unfollow"])
            follow_to_delete = get_object_or_404(UserFollowing, user=user, following_user=user_to_follow)
            follow_to_delete.delete()
            return redirect('profile', username=user_to_follow.username)

@login_required
@csrf_exempt
def like_unlike(request):
    data = json.loads(request.body)

    try:
        post = Post.objects.get(pk=data["id"])
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    if request.method == "POST":
        # create a like entry
        Like(user=request.user, post=post).save()
        return JsonResponse({'message': 'post success'})
    
    if request.method == "DELETE":
        # delete like entry
        like = get_object_or_404(Like, post=post, user=request.user)
        like.delete()

        return JsonResponse({'message': 'delete success'})

def update_post(request, post_id):
    if request.method != "PUT":
        return JsonResponse({'error': 'Put request required'}, status=400)
    
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    data = json.loads(request.body)
    if data["content"] == '':
        return JsonResponse({'error': 'Post must not be empty'}, status=400)
    
    if post.user != request.user:
        return JsonResponse({'error': "Can not edit other user's posts"}, status=400)
        
    post.content = data['content']
    post.save()
    return JsonResponse({'message': "put success"})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
