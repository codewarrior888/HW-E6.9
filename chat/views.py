from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from rest_framework import viewsets, permissions

from .forms import SignUpForm, UserUpdateForm, AccountUpdateForm
from .models import Room, Message
from .serializers import RoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAdminUser]


@login_required
def index(request):
    users = User.objects.exclude(pk=request.user.id)
    rooms = Room.objects.all()
    return render(request, 'index.html', {
        "users": users, 
        "rooms": rooms,
        })


@login_required
def room(request, room_name):
    room_object, created = Room.objects.get_or_create(room_name=room_name, defaults={'created_by': request.user})
    chats = Message.objects.filter(room=room_object) if not created else []
    return render(request, "room.html", {"room_name": room_name, 'chats': chats})


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def delete_room(request, room_name):
    room = get_object_or_404(Room, room_name=room_name)
    
    if request.user.is_superuser or room.created_by == request.user:
        room.delete()
        messages.success(request, f'Room {room_name} has been deleted.')
    else:
        messages.error(request, 'You do not have permission to delete this room.')

    return redirect('index')


@login_required
def profile(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        account_update_form = AccountUpdateForm(request.POST, request.FILES, instance=request.user.account)
        if user_update_form.is_valid() and account_update_form.is_valid():
            user_update_form.save()
            account_update_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('profile')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        account_update_form = AccountUpdateForm(instance=request.user.account)

    return render(request, 'profile.html', {
        'user_update_form': user_update_form,
        'account_update_form': account_update_form
    })
