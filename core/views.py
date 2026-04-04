from django.shortcuts import render
from rooms.models import Room

def home(request):
    featured_rooms = Room.objects.filter(is_active=True)[:3]
    return render(request, 'core/home.html', {'featured_rooms': featured_rooms})