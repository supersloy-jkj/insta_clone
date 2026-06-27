from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta

from .models import User, Follow
from .forms import RegisterForm, LoginForm, EditProfileForm
from stories.models import Story


def register_view(request):
    if request.user.is_authenticated:
        return redirect('posts:feed')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Instaclone, {user.username}!')
            return redirect('posts:feed')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('posts:feed')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.GET.get('next', 'posts:feed'))
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.posts.prefetch_related('media').order_by('-created_at')
    is_following = Follow.objects.filter(
        follower=request.user, followed=profile_user
    ).exists()
    has_active_stories = Story.objects.filter(
        author=profile_user,
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).exists()

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
        'has_active_stories': has_active_stories,
        'is_own_profile': request.user == profile_user,
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile', username=request.user.username)
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def follow_toggle(request, username):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    target = get_object_or_404(User, username=username)
    if target == request.user:
        return JsonResponse({'error': 'Cannot follow yourself'}, status=400)

    follow_obj, created = Follow.objects.get_or_create(
        follower=request.user, followed=target
    )
    if not created:
        follow_obj.delete()
        is_following = False
    else:
        is_following = True

    return JsonResponse({
        'is_following': is_following,
        'follower_count': target.follower_count,
    })


@login_required
def followers_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    followers = User.objects.filter(following__followed=profile_user)
    return render(request, 'users/follow_list.html', {
        'profile_user': profile_user,
        'users': followers,
        'list_type': 'Followers',
    })


@login_required
def following_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    following = User.objects.filter(followers__follower=profile_user)
    return render(request, 'users/follow_list.html', {
        'profile_user': profile_user,
        'users': following,
        'list_type': 'Following',
    })


@login_required
def search_view(request):
    query = request.GET.get('q', '').strip()
    users = []
    if query:
        users = User.objects.filter(
            username__icontains=query
        ).exclude(id=request.user.id)[:20]
    return render(request, 'users/search.html', {'users': users, 'query': query})
