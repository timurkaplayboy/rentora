from django.shortcuts import render, redirect
from django.contrib.auth import login
from rooms.models import Room
from .forms import RegisterForm


def home(request):
    featured_rooms = Room.objects.filter(is_active=True)[:3]
    return render(request, 'core/home.html', {'featured_rooms': featured_rooms})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='core.authentication.EmailOrUsernameBackend')
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})