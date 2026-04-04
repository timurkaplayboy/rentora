from django.contrib import admin
from .models import RoomType, Room


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'number', 'room_type', 'price_per_night', 'capacity', 'is_active')
    list_filter = ('room_type', 'is_active')
    search_fields = ('name', 'number')