from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from rooms.models import Room


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує'),
        ('confirmed', 'Підтверджено'),
        ('cancelled', 'Скасовано'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Бронювання'
        verbose_name_plural = 'Бронювання'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.full_name} - {self.room.name}'

    def clean(self):
        if not self.room_id:
            return

        if not self.start_date or not self.end_date:
            return

        if self.start_date >= self.end_date:
            raise ValidationError('Дата виїзду має бути пізніше за дату заїзду.')

        overlapping_bookings = Booking.objects.filter(
            room=self.room,
            status__in=['pending', 'confirmed'],
            start_date__lt=self.end_date,
            end_date__gt=self.start_date,
        ).exclude(pk=self.pk)

        if overlapping_bookings.exists():
            raise ValidationError('Ця кімната вже зайнята на обраний період.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)