from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms import ModelForm

from .models import *


class NewListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "category", "starting_price", "photo_url"]

    
class NewCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


class NewBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["offer"]


def index(request):
    return render(request, "auctions/index.html",
    {
        "listings": Listing.objects.all(),
        "title": "Watchlist",
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
            return HttpResponseRedirect(reverse("active_listings"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("active_listings"))


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
        return HttpResponseRedirect(reverse("active_listings"))
    else:
        return render(request, "auctions/register.html")


def active_listings(request):
    category = request.GET.get("category", None)
    if category:
        listings = Listing.objects.filter(expired=False, category=category)    
    else:
        listings = Listing.objects.filter(expired=False)

    return render(request, "auctions/index.html", 
    {
        "listings": listings,
        "title": "Active Listings",
        "categories": Category.objects.all()
    })


@login_required(login_url="login")
def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    return render(request, "auctions/listing.html", 
    {
        "listing": listing,
        "bid_form": NewBidForm(),
        "comment_form": NewCommentForm(),
        "comments": listing.comments.all(),
        "watchers": listing.watchers.all()
    })


@login_required(login_url="login")
def new_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST, request.FILES)

        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.seller = request.user
            new_listing.save()

            return render(request, "auctions/new_listing.html", 
            {
                "form": NewListingForm(),
                "flag": True
            })

        else:
            return render(request, "auctions/new_listing.html", 
            {
                "form": NewListingForm()
            })

    else:
        return render(request, "auctions/new_listing.html", 
        {
            "form": NewListingForm()
        })


def close_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.expired = True
    listing.save()
    return redirect("listing", listing_id=listing_id)


@login_required(login_url="login")
def watchlist(request):
    listings = request.user.watching.all()
    categories = Category.objects.all()
    return render(request, "auctions/index.html", 
    {
        "listings": listings,
        "title": "Watchlist",
        "categories": categories
    })


@login_required(login_url="login")
def update_watchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.user in listing.watchers.all():
        listing.watchers.remove(request.user)
    else:
        listing.watchers.add(request.user)
    return redirect("listing", listing_id=listing_id)    


@login_required(login_url="login")
def comment(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    form = NewCommentForm(request.POST)
    comment = form.save(commit=False)
    comment.user, comment.listing = request.user, listing
    comment.save()
    return redirect("listing", listing_id=listing_id)


@login_required(login_url="login")
def new_bid(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    offer = float(request.POST["offer"])

    if valid_bid(listing, offer):
        listing.current_offer = offer
        listing.buyer = request.user
        form = NewBidForm(request.POST)
        bid = form.save(commit=False)
        bid.listing, bid.user = listing, request.user
        bid.save()
        listing.save()
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid_form":  NewBidForm(),
            "comment_form": NewCommentForm(),
            "comments": listing.comments.all(),
            "watchers": listing.watchers.all(),
            "valid_offer": True
        })

    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid_form":  NewBidForm(),
            "comment_form": NewCommentForm(),
            "comments": listing.comments.all(),
            "watchers": listing.watchers.all(),
            "valid_offer": False
        })


def valid_bid(listing, offer):
    current_offer = listing.current_offer if listing.current_offer else 0
    return True if offer >= listing.starting_price and offer > current_offer else False