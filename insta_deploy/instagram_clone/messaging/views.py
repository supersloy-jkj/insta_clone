from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages as django_messages

from .models import Conversation, Message
from users.models import User


@login_required
def inbox_view(request):
    conversations = request.user.conversations.prefetch_related(
        'participants', 'messages'
    )
    conv_data = []
    for conv in conversations:
        other = conv.get_other_participant(request.user)
        last_msg = conv.last_message
        unread = conv.unread_count_for(request.user)
        conv_data.append({
            'conv': conv,
            'other': other,
            'last_msg': last_msg,
            'unread': unread,
        })

    return render(request, 'messaging/inbox.html', {'conv_data': conv_data})


@login_required
def new_conversation(request, username):
    other_user = get_object_or_404(User, username=username)
    if other_user == request.user:
        return redirect('messaging:inbox')

    # Find existing DM between the two users
    conv = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()

    if not conv:
        conv = Conversation.objects.create()
        conv.participants.add(request.user, other_user)

    return redirect('messaging:conversation', conv_id=conv.id)


@login_required
def conversation_view(request, conv_id):
    conv = get_object_or_404(Conversation, id=conv_id, participants=request.user)
    other_user = conv.get_other_participant(request.user)

    # Mark all incoming as read
    conv.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    all_messages = conv.messages.select_related('sender').all()

    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        media = request.FILES.get('media')

        if text or media:
            msg = Message.objects.create(
                conversation=conv,
                sender=request.user,
                text=text,
            )
            if media:
                msg.media = media
                msg.save()

            # Bump conversation's updated_at
            conv.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'id': msg.id,
                    'text': msg.text,
                    'media_url': msg.media.url if msg.media else None,
                    'sender': msg.sender.username,
                    'created_at': msg.created_at.strftime('%H:%M'),
                    'is_own': True,
                })
        return redirect('messaging:conversation', conv_id=conv_id)

    context = {
        'conv': conv,
        'messages': all_messages,
        'other_user': other_user,
    }
    return render(request, 'messaging/conversation.html', context)


@login_required
def poll_messages(request, conv_id):
    """AJAX long-poll endpoint: returns new messages since last_id."""
    conv = get_object_or_404(Conversation, id=conv_id, participants=request.user)
    last_id = int(request.GET.get('last_id', 0))

    new_msgs = conv.messages.filter(id__gt=last_id).exclude(
        sender=request.user
    ).select_related('sender')

    # Mark as read
    new_msgs.filter(is_read=False).update(is_read=True)

    data = [{
        'id': msg.id,
        'text': msg.text,
        'media_url': msg.media.url if msg.media else None,
        'sender': msg.sender.username,
        'sender_pic': msg.sender.get_profile_picture_url(),
        'created_at': msg.created_at.strftime('%H:%M'),
    } for msg in new_msgs]

    return JsonResponse({'messages': data})
