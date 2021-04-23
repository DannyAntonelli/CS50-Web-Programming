from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Profile, Post

import json


def index(request):
    return render(request, "network/index.html")


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


@login_required(login_url="login")
def new_post(request):
    # New post
    if request.method == "POST":
        text = request.POST["text"]
        post = Post(text=text)
        post.user = request.user
        post.save()
    
    # Edit post
    elif request.method == "PUT":
        data = json.loads(request.body)
        id = data["id"]
        post = Post.objects.get(id=id)
        
        # Unauthorized
        if post.user != request.user:
            return HttpResponse(status=401)

        text = data["text"]
        post.text = text
        post.save()
        
    else:
        return JsonResponse({"error": "POST or PUT request required"}, status=400)

    return HttpResponseRedirect(reverse("index"))


def get_posts(request, num_page):
    user = request.GET.get("user")
    posts = user.get_posts.all() if user else Post.objects.all()
    return load_paginated_posts(request, posts, num_page)


@login_required(login_url="login")
def get_following_posts(request, num_page):
    following = request.user.following.all()
    following = [profile.user for profile in following]
    posts = Post.objects.filter(user__in=following).all()
    return load_paginated_posts(request, posts, num_page)


def get_profile_posts(request, id, num_page):
    profile = Profile.objects.filter(id=id).first()
    posts = profile.user.get_posts
    return load_paginated_posts(request, posts, num_page)


def load_paginated_posts(request, posts, num_page):
    POSTS_PER_PAGE = 10
    ordered_posts = posts.order_by("-timestamp").all()  
    paginator = Paginator(ordered_posts, POSTS_PER_PAGE)
    page = paginator.get_page(num_page)
    return JsonResponse({
        "posts": [post.serialize(request.user) for post in page],
        "numPages": paginator.num_pages
        })


def get_profile(request, id):
    profile = Profile.objects.filter(id=id).first()
    return JsonResponse(profile.serialize(request.user))


@login_required(login_url="login")
def change_like(request, id):
    post = Post.objects.get(id=id)
    liked = post in request.user.get_likes.all()

    if liked:
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    post.save()

    return JsonResponse({
        "liked": not liked,
        "numLikes": post.likes.count()
    })


@login_required(login_url="login")
def change_follow(request, id):
    profile = Profile.objects.get(id=id)
    following = profile in request.user.following.all()

    if following:
        profile.followers.remove(request.user)
    else:
        profile.followers.add(request.user)
    
    profile.save()
    return JsonResponse({
        "following": not following,
        "numFollowers": profile.followers.count()
    })