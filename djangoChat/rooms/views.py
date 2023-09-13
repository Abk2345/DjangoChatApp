from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required

from .models import Room, Message, PersonalMessage

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse

# list of chat rooms
@login_required
def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/rooms.html', {'rooms': rooms})

# messages of chat room, detail view of chat room
@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)
    return render(request, 'rooms/room.html', {'room': room, 'messages':messages})

# homepage
def home(request):
    return render(request, 'rooms/home.html')

# all active users except currently logged in
@login_required
def get_active_users(request):
    current_user = request.user
    # Get all active sessions
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())

    # Extract user IDs from active sessions
    user_ids = [session.get_decoded().get('_auth_user_id') for session in active_sessions]

    # Query the User model to get user objects for active users
    active_users = User.objects.filter(id__in=user_ids)

    active_users_except_current = active_users.exclude(id=current_user.id)

    # print(active_users)

    # You can now use active_users in your template or return it as JSON data
    return render(request, 'rooms/active_users.html', {'active_users': active_users_except_current})

# messages of personal chat, personal chat detail view
@login_required
def personalChatUser(request, username):
    friend = get_object_or_404(User, username=username)
  
    messages = PersonalMessage.objects.filter(
        sender=request.user,
        recipient=friend
    ) | PersonalMessage.objects.filter(
        sender=friend,
        recipient=request.user
    ).order_by('timestamp')

    # print(friend, messages)

    return render(request, 'rooms/personal_chat.html', {'friend': friend, 'messages':messages})