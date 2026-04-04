from django.shortcuts import render, get_object_or_404
from .models import Room, RoomType


def room_list(request):
    rooms = Room.objects.filter(is_active=True)
    room_types = RoomType.objects.all()

    room_type_id = request.GET.get('type')
    guests = request.GET.get('guests')

    if room_type_id:
        rooms = rooms.filter(room_type_id=room_type_id)

    if guests:
        try:
            rooms = rooms.filter(capacity__gte=int(guests))
        except ValueError:
            pass

    context = {
        'rooms': rooms,
        'room_types': room_types,
    }
    return render(request, 'rooms/room_list.html', context)


def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk, is_active=True)
    return render(request, 'rooms/room_detail.html', {'room': room})