from django.urls import path
from .views import room_list, room_detail

urlpatterns = [
    path('', room_list, name='room_list'),
    path('<int:pk>/', room_detail, name='room_detail'),
]