from django.urls import path
from .views import create_booking, check_availability, my_bookings, booking_success

urlpatterns = [
    path('room/<int:room_id>/create/', create_booking, name='create_booking'),
    path('room/<int:room_id>/check/', check_availability, name='check_availability'),
    path('my/', my_bookings, name='my_bookings'),
    path('success/', booking_success, name='booking_success'),
]