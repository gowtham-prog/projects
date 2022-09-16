from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import *

from django.contrib.auth.decorators import login_required

import json

from django.core.paginator import Paginator

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
            Profile(user=user).save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def save_post(request):
    if request.method == "POST":
        form = Post(content=request.POST['content'])    
        form.creator = Profile.objects.get(user=request.user)
        form.save()
    elif request.method == "PUT":
        data = json.loads(request.body)        
        post_id = int(data["post_id"])
        new_content = data["new_content"]
        post = Post.objects.filter(id=post_id).first()     
        if post.creator.user != request.user:
            return HttpResponse(status=401)
        post.content = new_content
        post.save()
        return JsonResponse({
            "result": True
        },status=200)
    else:
        return JsonResponse({
                "error": f"request methods supported: POST, GET"
            }, status=400)
    return index(request)

@login_required
def load_followed_posts(request):
    followed_profiles = request.user.get_followed_profiles.all()
    print(followed_profiles)
    posts = Post.objects.filter(creator__in=followed_profiles).all()
    return paginated_posts(request,posts)

def load_posts(request): 
    profile = request.GET.get("profile", None)
    if (profile):
        posts = Post.objects.filter(creator=profile).all()
    else:
        posts = Post.objects.all()     
    return paginated_posts(request,posts)

def paginated_posts(request,posts):
    posts = posts.order_by("-created_date").all()  
    paginator = Paginator(posts,10)
    page_obj = paginator.get_page(request.GET["page"])
    return JsonResponse({
        "posts": [post.serialize(request.user) for post in page_obj],
        "num_pages": paginator.num_pages
        }
        , safe=False)


def profile(request,user_id):
    profile = Profile.objects.filter(id=user_id).first()
    return JsonResponse(profile.serialize(request.user),status=200)

@login_required 
def update_like(request,post_id):
    profile = Profile.objects.filter(user=request.user).first()
    post = Post.objects.get(id=post_id)
    if post in profile.get_all_liked_posts.all():
        newStatus = False
        post.likes.remove(profile)
    else:
        newStatus = True
        post.likes.add(profile)
    post.save()
    return JsonResponse({"liked": newStatus, "newAmount": post.likes.count()},status=200)

@login_required 
def update_follow(request,profile_id):
    profile = Profile.objects.get(id=profile_id)
    if profile in request.user.get_followed_profiles.all():
        newStatus = False
        profile.followers.remove(request.user)
    else:
        newStatus = True
        profile.followers.add(request.user)
    profile.save()
    return JsonResponse({"newFollower": newStatus, "newAmount": profile.followers.count()},status=200)