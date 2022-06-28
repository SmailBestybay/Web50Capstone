from email import message
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import User, Listing, Watchlist, Bid
from .formhelper import NewListingForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    # active listings should display
    # title, description, starting bid, current price, photo(if exists)
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
        })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login')
def create_listing(request):
    if request.method == "POST":
        # https://docs.djangoproject.com/en/4.0/topics/forms/
        # instantiate bound form 
        form = NewListingForm(request.POST)
        if form.is_valid():
            
            # instantiate every field
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            image = form.cleaned_data["image"]
            category = form.cleaned_data["category"]
            # get id of the user creating the listing.
            # all model instances have id so need user.id
            # but in our case we need an instance of a user as a whole.
            owner = request.user

            # instantiate an object of models class
            listing = Listing(
                title=title,
                description=description, 
                starting_bid=starting_bid,
                image=image,
                category=category,
                owner=owner
                )
            # https://docs.djangoproject.com/en/4.0/ref/models/instances/#saving-objects
            listing.save()
            return redirect("listing", listing.id)
        
        else:
            return render(request, "auctions/create_listing.html", {
                "form": form
            })

    return render(request, "auctions/create_listing.html", {
        "form" : NewListingForm()
    })

def listing(request, listing_id):
    
    # TODO        
    # if signed it and creator, able to close listing
    # if closed, make highest bidder the winner
    # if closed, make listing not active
    # if signed in on closed listing, display if user won.
    # display comments
    # if signed in, able to add comments

    listing = get_object_or_404(Listing, pk=listing_id)
    try:
        watchlist_item = listing.watchlisted.get(user=request.user.id)
        watchlisted = True
    except ObjectDoesNotExist:
        watchlist_item = None
        watchlisted = False
    # all bids on this listing
    bids = Bid.objects.all().filter(listing=listing)
    highest_bid = bids.first()

    for bid in bids:
        if bid.amount > highest_bid.amount and bid.amount > listing.starting_bid:
            highest_bid = get_object_or_404(Bid, pk=bid.id)

    
    if request.method == "POST":
        if "add_or_remove" in request.POST:
            # using get_or_create method in order to avoid saving twice
            watchlist_item, created = Watchlist.objects.get_or_create(
                user=request.user,
                listing=listing
            )
            if not created:
                watchlist_item.delete()
            return redirect("listing", listing.id)
        
        if "bid" in request.POST:
            placed_bid = request.POST["bid"]
            if placed_bid == "":
                return redirect("listing", listing.id)

            # need if no bids have been placed yet.
            elif highest_bid == None and int(placed_bid) > listing.starting_bid:
                Bid(user=request.user, listing=listing, amount=placed_bid).save()
                return redirect("listing", listing.id)

            elif int(placed_bid) > highest_bid.amount:
                Bid(user=request.user, listing=listing, amount=placed_bid).save()
                return redirect("listing", listing.id)

            else:
                return render(request, "auctions/listing.html", {
                    "listing" : listing,
                    "watchlisted" : watchlisted,
                    "watchlist_item" : watchlist_item,
                    "bids" : bids,
                    "highest_bid" : highest_bid,
                    "message" : "Bid amount must be higher then starting and current bid"
                })

        if "close_listing" in request.POST:
            listing.closed = True
            #TODO get bid objects with highest bid
            bid = get_object_or_404(Bid, pk=request.POST["close_listing"])
            listing.winner = bid.user
            listing.save()
            return redirect("listing", listing.id)

    return render(request, "auctions/listing.html", {
        "listing" : listing,
        "watchlisted" : watchlisted,
        "watchlist_item" : watchlist_item,
        "bids" : bids,
        "highest_bid" : highest_bid
    })

@login_required(login_url='login')
def watchlist(request):
    # display signed in user's watchlist
    # each item in list links to listing
    # able to remove from watchlist
    user = request.user
    watchlist = Watchlist.objects.all().filter(user=user)
    listings = []

    for item in watchlist:
        listings.append(item.listing)

    
    return render(request, "auctions/watchlist.html", {
        "listings" : listings
    })

def categories(request):
    # Display list of categories
    # item in list is link to list of active listings in category
    pass