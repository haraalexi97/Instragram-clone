from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Comment, Follow, Like, Post, Profile

def feed(request):
    posts = Post.objects.select_related("author").prefetch_related("likes", "comments__user")
    if request.user.is_authenticated:
        ids = Follow.objects.filter(follower=request.user).values_list("followed_id", flat=True)
        posts = posts.filter(Q(author_id__in=ids) | Q(author=request.user))
    return render(request, "social/feed.html", {"posts": posts[:50]})

def signup(request):
    if request.user.is_authenticated: return redirect("feed")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        Profile.objects.get_or_create(user=user)
        login(request, user)
        messages.success(request, "Welcome! Your account is ready.")
        return redirect("feed")
    return render(request, "registration/signup.html", {"form": form})

@login_required
def create_post(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        if image:
            Post.objects.create(author=request.user, image=image, caption=request.POST.get("caption", "").strip()[:2200])
            messages.success(request, "Photo shared.")
            return redirect("feed")
        messages.error(request, "Choose a photo first.")
    return render(request, "social/create_post.html")

@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created: like.delete()
    return redirect(request.POST.get("next") or "feed")

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    text = request.POST.get("text", "").strip()
    if text: Comment.objects.create(user=request.user, post=post, text=text[:500])
    return redirect(request.POST.get("next") or "feed")

def profile(request, username):
    person = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=person)
    following = request.user.is_authenticated and Follow.objects.filter(follower=request.user, followed=person).exists()
    return render(request, "social/profile.html", {"profile_user": person, "posts": posts,
      "post_count": posts.count(), "followers_count": Follow.objects.filter(followed=person).count(),
      "following_count": Follow.objects.filter(follower=person).count(), "is_following": following})

@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        request.user.first_name = request.POST.get("first_name", "").strip()[:150]
        request.user.last_name = request.POST.get("last_name", "").strip()[:150]
        request.user.save()
        profile.bio = request.POST.get("bio", "").strip()[:160]
        if request.FILES.get("avatar"): profile.avatar = request.FILES["avatar"]
        profile.save()
        messages.success(request, "Profile updated.")
        return redirect("profile", username=request.user.username)
    return render(request, "social/edit_profile.html", {"profile_obj": profile})

@login_required
@require_POST
def toggle_follow(request, username):
    person = get_object_or_404(User, username=username)
    if person != request.user:
        link, created = Follow.objects.get_or_create(follower=request.user, followed=person)
        if not created: link.delete()
    return redirect("profile", username=username)

def explore(request):
    query = request.GET.get("q", "").strip()
    users = User.objects.all()
    if request.user.is_authenticated: users = users.exclude(pk=request.user.pk)
    if query: users = users.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
    return render(request, "social/explore.html", {"users": users[:30], "posts": Post.objects.select_related("author")[:60], "query": query})
