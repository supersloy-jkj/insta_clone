import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .models import Story, StoryView
from users.models import User, Follow


@login_required
def create_story_view(request):
    if request.method == 'POST':
        media_file = request.FILES.get('media')
        caption = request.POST.get('caption', '')

        if not media_file:
            messages.error(request, 'Please select a photo or video.')
            return render(request, 'stories/create_story.html')

        ext = os.path.splitext(media_file.name)[1].lower()
        media_type = 'video' if ext in ['.mp4', '.mov', '.avi', '.webm', '.mkv'] else 'image'

        Story.objects.create(
            author=request.user,
            media=media_file,
            media_type=media_type,
            caption=caption,
        )
        messages.success(request, 'Story posted! It will expire in 24 hours.')
        return redirect('posts:feed')

    return render(request, 'stories/create_story.html')


@login_required
def view_story(request, username):
    story_user = get_object_or_404(User, username=username)
    since = timezone.now() - timedelta(hours=24)
    stories = Story.objects.filter(author=story_user, created_at__gte=since)

    if not stories.exists():
        messages.info(request, 'No active stories.')
        return redirect('posts:feed')

    # Record views (not for own stories)
    if story_user != request.user:
        for story in stories:
            StoryView.objects.get_or_create(story=story, viewer=request.user)

    # Find next user with active stories (for chaining)
    following_ids = Follow.objects.filter(
        follower=request.user
    ).values_list('followed_id', flat=True)

    next_user = User.objects.filter(
        id__in=following_ids,
        stories__created_at__gte=since,
    ).exclude(id=story_user.id).distinct().first()

    context = {
        'story_user': story_user,
        'stories': list(stories),
        'next_user': next_user,
        'is_own_story': request.user == story_user,
        'view_counts': [s.view_count for s in stories],
    }
    return render(request, 'stories/view_story.html', context)


@login_required
def delete_story(request, story_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)
    if request.method == 'POST':
        story.delete()
        messages.success(request, 'Story deleted.')
    return redirect('posts:feed')
