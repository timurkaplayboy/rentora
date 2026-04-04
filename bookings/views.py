from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from rooms.models import Room
from .forms import BookingForm
from .models import Booking


@login_required
def create_booking(request, room_id):
    room = get_object_or_404(Room, pk=room_id, is_active=True)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.save()

            send_mail(
                subject='Підтвердження створення бронювання',
                message=(
                    f'Ваше бронювання для кімнати "{room.name}" створено.\n'
                    f'Період: {booking.start_date} - {booking.end_date}\n'
                    f'Статус: {booking.get_status_display()}'
                ),
                from_email=None,
                recipient_list=[booking.email],
                fail_silently=True,
            )

            messages.success(request, 'Бронювання успішно створено.')
            return redirect('booking_success')
    else:
        initial_data = {
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        }
        form = BookingForm(initial=initial_data)

    return render(request, 'rooms/room_detail.html', {
        'room': room,
        'form': form,
    })


def check_availability(request, room_id):
    room = get_object_or_404(Room, pk=room_id, is_active=True)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not start_date or not end_date:
        return JsonResponse({
            'available': False,
            'message': 'Вкажіть дату заїзду і виїзду.'
        })

    overlapping = Booking.objects.filter(
        room=room,
        status__in=['pending', 'confirmed'],
        start_date__lt=end_date,
        end_date__gt=start_date,
    ).exists()

    if overlapping:
        return JsonResponse({
            'available': False,
            'message': 'Кімната недоступна на цей період.'
        })

    return JsonResponse({
        'available': True,
        'message': 'Кімната доступна.'
    })


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


def booking_success(request):
    return render(request, 'bookings/booking_success.html')