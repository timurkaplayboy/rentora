from django.db import models


class RoomType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Тип кімнати'
        verbose_name_plural = 'Типи кімнат'

    def __str__(self):
        return self.name


class Room(models.Model):
    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.CASCADE,
        related_name='rooms'
    )
    name = models.CharField(max_length=150)
    number = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    features = models.TextField(blank=True, help_text='Наприклад: Wi-Fi, balcony, minibar')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Кімната'
        verbose_name_plural = 'Кімнати'
        ordering = ['number']

    def __str__(self):
        return f'{self.name} ({self.number})'