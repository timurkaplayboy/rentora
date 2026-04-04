from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'room', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('status', 'room')
    search_fields = ('full_name', 'email')
    list_editable = ('status',)