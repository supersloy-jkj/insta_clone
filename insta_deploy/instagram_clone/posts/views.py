import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta

from .models import Post, PostMedia, Like, Comment, SavedPost
from .forms import PostCreateForm, CommentForm
from users.models import User, Follow
from stories.models import Story


@login_required
def feed_view(request):
    following_ids = list(
        Follow.objects.filter(follower=request.user).values_list('followed_id', flat=True)
    )
    posts = Post.objects.filter(
        author_id__in=following_ids + [request.user.id]
    ).select_related('author').prefetch_related('media', 'likes', 'comments')

    # Stories bar: users you follow who have active stories
    since = timezone.now() - timedelta(hours=24)
    story_users = User.objects.filter(
        id__in=following_ids,
        stories__created_at__gte=since
    ).distinct()

    # Own story status
    has_own_story = Story.objects.filter(
        author=request.user, created_at__gte=since
    ).exists()

    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    liked_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
    saved_ids = set(SavedPost.objects.filter(user=request.user).values_list('post_id', flat=True))

    context = {
        'page_obj': page_obj,
        'story_users': story_users,
        'has_own_story': has_own_story,
        'liked_ids': liked_ids,
        'saved_ids': saved_ids,
        'comment_form': CommentForm(),
    }
    return render(request, 'posts/feed.html', context)


@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            files = request.FILES.getlist('media_files')
            if not files:
                post.delete()
                messages.error(request, 'Please add at least one photo or video.')
                return render(request, 'posts/create_post.html', {'form': form})

            for i, file in enumerate(files):
                ext = os.path.splitext(file.name)[1].lower()
                media_type = 'video' if ext in ['.mp4', '.mov', '.avi', '.webm', '.mkv'] else 'image'
                PostMedia.objects.create(post=post, file=file, media_type=media_type, order=i)

            messages.success(request, 'Post shared!')
            return redirect('posts:feed')
    else:
        form = PostCreateForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(
        post=post, parent=None
    ).select_related('user').prefetch_related('replies__user')

    is_liked = Like.objects.filter(user=request.user, post=post).exists()
    is_saved = SavedPost.objects.filter(user=request.user, post=post).exists()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = get_object_or_404(Comment, id=parent_id)
            comment.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'username': comment.user.username,
                    'profile_pic': comment.user.get_profile_picture_url(),
                    'text': comment.text,
                    'comment_id': comment.id,
                })
            return redirect('posts:post_detail', post_id=post.id)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'is_liked': is_liked,
        'is_saved': is_saved,
        'comment_form': form,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('users:profile', username=request.user.username)
    return render(request, 'posts/confirm_delete.html', {'post': post})


@login_required
def like_toggle(request, post_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    post = get_object_or_404(Post, id=post_id)
    like_obj, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like_obj.delete()
        is_liked = False
    else:
        is_liked = True
    return JsonResponse({'is_liked': is_liked, 'like_count': post.like_count})


@login_required
def save_toggle(request, post_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    post = get_object_or_404(Post, id=post_id)
    save_obj, created = SavedPost.objects.get_or_create(user=request.user, post=post)
    if not created:
        save_obj.delete()
        is_saved = False
    else:
        is_saved = True
    return JsonResponse({'is_saved': is_saved})


@login_required
def saved_posts_view(request):
    saved = SavedPost.objects.filter(
        user=request.user
    ).select_related('post__author').prefetch_related('post__media')
    return render(request, 'posts/saved_posts.html', {'saved': saved})
